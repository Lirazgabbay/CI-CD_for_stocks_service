"""
    stock_service.py - This module contains the functions to interact with the stock price API.
"""
from .api_operations import ApiOperations
from .portfolio_error import PortfolioError
import requests

API_KEY = "rIIN301/cz821UxjwhsXrw==Oh9mnMbgYJpNAimx"
BASE_URL = f'https://api.api-ninjas.com'

def get_current_stock_price(symbol):
    endpoint = f'v1/stockprice?ticker={symbol}'
    response =  ApiOperations.get_request(BASE_URL, endpoint,
                                     headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        json_response = response.json()

        if isinstance(json_response, list) and len(json_response) > 0:
            return json_response[0].get('price')  # Access the first item in the list
        elif isinstance(json_response, list) and len(json_response) == 0:
            raise PortfolioError.api_server_error(f"Symbol '{symbol}' not found in the API")
        elif isinstance(json_response, dict):
            return json_response.get('price')
        else:
            raise PortfolioError.api_server_error("Unexpected API response format")
    else:
        raise PortfolioError.api_server_error(response.status_code)

