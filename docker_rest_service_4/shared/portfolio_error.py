from flask import jsonify

class PortfolioError(Exception):
    """Custom error class for consistent JSON error responses and exception handling."""

    def __init__(self, message, status_code=500, key_error="server error"):
        """Initialize the error with a message, status code, and key."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.key_error = key_error

    def to_response(self):
        """Convert the error into a JSON response."""
        return jsonify({self.key_error: self.message}), self.status_code

    # Static helper methods for common errors
    @staticmethod
    def malformed_data(raise_exception=False):
        if raise_exception:
            raise PortfolioError("Malformed data", 400, "error")
        return PortfolioError("Malformed data", 400, "error").to_response()

    @staticmethod
    def not_found(raise_exception=False):
        if raise_exception:
            raise PortfolioError("Resource not found", 404, "error")
        return PortfolioError("Resource not found", 404, "error").to_response()

    @staticmethod
    def unsupported_media_type(raise_exception=False):
        if raise_exception:
            raise PortfolioError("Expected application/json media type", 415, "error")
        return PortfolioError("Expected application/json media type", 415, "error").to_response()

    @staticmethod
    def server_error(exception, raise_exception=False):
        if raise_exception:
            raise PortfolioError(str(exception), 500, "server error")
        return PortfolioError(str(exception), 500, "server error").to_response()

    @staticmethod
    def api_server_error(status_code, raise_exception=False):
        if raise_exception:
            raise PortfolioError(f"API response code {status_code}", 500, "server error")
        return PortfolioError(f"API response code {status_code}", 500, "server error").to_response()
