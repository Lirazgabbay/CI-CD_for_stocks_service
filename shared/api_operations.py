import requests

class ApiOperations:
    """
    ApiOperations provides static methods for common HTTP operations,
    including GET and POST requests and response handling.
    """

    @staticmethod
    def get_request(base_url, endpoint, headers={}, params={}):
        url = f"{base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)

        return response



