"""
    This is the main entry point for the stocks service. 
"""
from flask import Flask
from routes import register_routes
import os
from utils.db import DB

def create_app():
    """
        Create and configure the Flask app.
    """
    app = Flask(__name__)
    register_routes(app)
    return app

if __name__ == '__main__':
    service_type = os.environ.get("SERVICE_TYPE") 

    if service_type == "stocks1" or service_type == "stocks2":
        # Initialize and connect to the MongoDB for stocks services
        db = DB()
        db.connect()
        port = int(os.environ.get("STOCK_SERVICE_PORT", 8000))
    else:
        raise RuntimeError("Unknown SERVICE_TYPE specified")

    app = create_app()
    app.run(host='0.0.0.0', port=port)
