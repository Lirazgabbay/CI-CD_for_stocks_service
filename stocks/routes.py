"""
    routes.py: This file contains the routes for the stocks service.
"""
from datetime import datetime
import os
from bson import ObjectId
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from models.stock import Stock
from shared.portfolio_error import PortfolioError
from shared.stock_service import get_current_stock_price
from utils.db import DB 
from validators import validate_json_request, validate_required_fields, validate_date

def get_db_connection():
    """"
        establishes a connection to the database.
    """
    try:
        db_instance = DB()
        db_instance.connect()
        return db_instance.db
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def register_routes(app):
    """
        Registers the routes for the stocks service.
    """
    db = None
    db_instance = DB()
    
    try:
        db_instance.connect()
        database_name = os.environ.get("DATABASE_NAME")
        db = db_instance.client[database_name]

    except Exception as e:
        return PortfolioError.server_error(f"Failed to connect to MongoDB: {e}")
    
    if db is None:
        return PortfolioError.server_error("connection is not available.")
    
    collection = os.environ.get("SERVICE_TYPE", "stocks")
    stocks_collection = db[collection]  

    @app.route('/stocks', methods=['POST', 'GET'])
    def manage_stocks():
        """"
            Manages the post and get requests for the stocks service.
        """
        try:
            if request.method == 'POST':
                if not request.is_json:
                    return PortfolioError.unsupported_media_type()
                
                try:
                    data = request.get_json()
                except BadRequest:
                    return PortfolioError.malformed_data()

                required_fields = ['symbol', 'purchase price', 'shares']
                if not all(field in data for field in required_fields):
                    return PortfolioError.malformed_data()

                # Create and store the stock
                try:
                    stock = Stock(
                        symbol= data['symbol'],
                        purchase_price= data['purchase price'],
                        shares= data['shares'],
                        name= data.get('name', 'NA'),
                        purchase_date= data.get('purchase date', 'NA'),
                    )
                except PortfolioError as e:  
                    return e  # PortfolioError.malformed_data() should return a 400 response
                
                result = stocks_collection.insert_one(stock.to_dict()) 
                return jsonify({'id': str(result.inserted_id)}), 201
            
            elif request.method == 'GET':
                try:
                    query_params = request.args.to_dict()
                    mongo_query = {}
                    for key, value in query_params.items():
                        if key == 'purchase_price':
                            mongo_query[key] = float(value) 
                        elif key == 'shares':
                            mongo_query[key] = int(value)  
                        else:
                            mongo_query[key] = value  

                    stocks = list(stocks_collection.find(mongo_query))
                    for stock in stocks:
                        stock['id'] = str(stock.pop('_id'))
                    
                    return jsonify(stocks), 200
                except Exception as e:
                    return PortfolioError.server_error(e)
                
        except KeyError as e:
            return PortfolioError.malformed_data()
        except Exception as e:
            return PortfolioError.server_error(e)


    @app.route('/stocks/<stock_id>', methods=['GET', 'DELETE', 'PUT'])
    def manage_stock(stock_id):
        """
            manages the get, delete and put requests for a stock by id.
        """
        try:
            stock_id = ObjectId(stock_id)

            stock = stocks_collection.find_one({"_id": stock_id})
            if not stock:
                return PortfolioError.not_found()

            if request.method == 'GET':
                stock['id'] = str(stock.pop('_id'))  
                return jsonify(stock), 200

            elif request.method == 'DELETE':
                try:
                    stocks_collection.delete_one({"_id": stock_id})
                    return '', 204
                except Exception as e:
                    return PortfolioError.server_error(e)

            elif request.method == 'PUT':
                if not request.is_json:
                    return PortfolioError.unsupported_media_type()
                data = validate_json_request()
                if isinstance(data,tuple):
                    return data
                if str(stock_id) != data.get('id'):
                    return PortfolioError.malformed_data()
                required_fields = ['name','purchase date','symbol', 'purchase price', 'shares', 'id']
                validate_required_fields(required_fields,data)
                try:
                    updated_stock = {
                    "symbol": data['symbol'],
                    "purchase_price": data['purchase price'],
                    "shares": data['shares'],
                    "name": data['name'],
                    "purchase_date": validate_date(str(data['purchase date'])),
                    }
                    stocks_collection.update_one({"_id": stock_id}, {"$set": updated_stock})
                    return jsonify({'id': str(stock_id)}), 200
                except Exception as e:
                    return PortfolioError.server_error(e)
        except Exception as e:
            return PortfolioError.server_error(e)

    @app.route('/stock-value/<stock_id>', methods=['GET'])
    def stock_value(stock_id):
        """
            responsible for getting the value of a stock by id.
        """
        try:
            stock_id = ObjectId(stock_id)
            stock = stocks_collection.find_one({"_id": stock_id})

            if not stock:
                return PortfolioError.not_found()
            
            current_price_external_API = get_current_stock_price(stock["symbol"])
            stock_value = round(current_price_external_API * stock["shares"], 2)
            return jsonify({
                "symbol": stock["symbol"],
                "ticker": current_price_external_API,
                "stock value": stock_value
            }), 200

        except Exception as e:
            return PortfolioError.server_error(e)
        
    @app.route('/portfolio-value', methods=['GET'])
    def portfolio_value():
        """
            responsible for getting the value of the entire portfolio.
        """
        try:
            total_value = 0.0
            stocks = list(stocks_collection.find()) 

            for stock in stocks:
                try:
                    current_price = get_current_stock_price(stock["symbol"])
                    total_value += current_price * stock["shares"]
                except Exception as e:
                    return PortfolioError.server_error(e)
                
            return jsonify({
                "date": datetime.now().strftime("%d-%m-%Y"),
                "portfolio value": round(total_value, 2)
            }), 200
        except Exception as e:
            return PortfolioError.server_error(e)
        
    @app.route('/kill', methods=['GET'])
    def kill_container():
        """
            Kills the container.
        """
        os._exit(1)