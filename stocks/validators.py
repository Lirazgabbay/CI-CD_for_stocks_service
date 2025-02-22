"""
    This module contains helper functions for validating input data.
"""
from datetime import datetime
from flask import request
from shared.portfolio_error import PortfolioError

def validate_json_request():
    """
    Validates that the request is a JSON request and returns the JSON payload.
    If invalid, returns the appropriate error response.
    """
    if not request.is_json:
        return PortfolioError.unsupported_media_type()
    data = request.get_json(silent=True)
    if data is None:
        return PortfolioError.malformed_data()
    return data


def validate_required_fields(required_fields, data):
    """
    Validates that all required fields are present in the data and are not empty.

    Args:
    required_fields : List of required field names.
    data : Dictionary of input data to validate.

    returns:
    True if all required fields are present and non-empty, raises PortfolioError otherwise.
    """
    # Check if all fields exist
    if not all(field in data for field in required_fields):
        raise PortfolioError.malformed_data()
    
    # Check if any field is empty (None, empty string, or only whitespace for strings)
    for field in required_fields:
        value = data[field]
        if value is None:
            raise PortfolioError.malformed_data()
        if isinstance(value, str) and not value.strip(): 
            raise PortfolioError.malformed_data()
    return True


def validate_date(date_str: str) -> str:
    """Validate that the date is in DD-MM-YYYY format."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y").date()  # Check if date matches DD-MM-YYYY format
        return date_str

    except ValueError:
        raise PortfolioError.malformed_data()




