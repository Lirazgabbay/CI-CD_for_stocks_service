import pytest
import requests

BASE_URL = "http://localhost:5001"

# Stocks data for testing
stock1 = {
    "name": "NVIDIA Corporation",
    "symbol": "NVDA",
    "purchase price": 134.66,
    "purchase date": "18-06-2024",
    "shares": 7
}

stock2 = {
    "name": "Apple Inc.",
    "symbol": "AAPL",
    "purchase price": 183.63,
    "purchase date": "22-02-2024",
    "shares": 19
}

stock3 = {
    "name": "Alphabet Inc.",
    "symbol": "GOOG",
    "purchase price": 140.12,
    "purchase date": "24-10-2024",
    "shares": 14
}


stock7 = {
    "name": "Amazon.com, Inc.",
    "purchase price": 134.66,
    "purchase date": "18-06-2024",
    "shares": 7
}


stock8 = {
    "name": "Amazon.com, Inc.",
    "symbol": "AMZN",
    "purchase price": 134.66,
    "purchase date": "Tuesday, June 18, 2024",
    "shares": 7
}


@pytest.fixture(scope="module")
def stock_ids():
    """Fixture to store stock IDs after creation."""
    return []


#test 1
def test_create_stocks(stock_ids):
    """Execute three POST /stock requests supplying the details of stock1, stock2, and stock3
    These tests are successful if
    (i) All 3 requests return unique IDs (none of the IDs are the same),
    (ii) The return status code from each POST request is 201"""
    
    stocks = [stock1, stock2, stock3]
    for stock in stocks:
        response = requests.post(f"{BASE_URL}/stocks", json=stock)
        assert response.status_code == 201
        stock_id = response.json().get("id")
        assert stock_id is not None
        stock_ids.append(stock_id)
    assert len(set(stock_ids)) == 3 , "Expected 3 unique stock IDs"


#test 2
def test_get_stock(stock_ids):
    """Execute a GET stocks/{ID} request, using the ID of stock1. 
    The test is successful if 
    (i) the symbol field equals “NVDA”, 
    (ii) the return status code from the request is 200."""
    stock_id = stock_ids[0]
    response = requests.get(f"{BASE_URL}/stocks/{stock_id}")
    assert response.status_code == 200
    assert response.json()["symbol"] == "NVDA" , "Expected symbol to be NVDA"


#test 3
def test_get_all_stocks():
    """Execute a GET /stocks request. 
    The test is successful if 
    (i) the returned JSON object has 3 embedded JSON objects (stocks), 
    (ii) the return status code from the GET request is 200."""
    response = requests.get(f"{BASE_URL}/stocks")
    assert response.status_code == 200, "Failed to retrieve stock data"
    stocks = response.json()
    assert isinstance(stocks, list) and len(stocks) == 3, "stocks should be a list with 3 elements"


#test 4
def test_stock_values(stock_ids):
    """Execute 3 GET /stock-value/{ID} requests using the IDs of stock1, stock2 and stock3. 
    Let sv1,sv2, and sv3 be the value of the “stock value” field returned from the 3 requests respectively. 
    The test is successful if 
    (i) the symbol field of each request equals ”NVDA”, “AAPL”, and “GOOG” respectively,
    (ii) the return status code from each request is 200"""
    expected_symbols = ["NVDA", "AAPL", "GOOG"]
    for idx, stock_id in enumerate(stock_ids):
        response = requests.get(f"{BASE_URL}/stock-value/{stock_id}")
        assert response.status_code == 200, f"Failed to get stock value for {expected_symbols[idx]}"
        stock_data = response.json()
        assert stock_data["symbol"] == expected_symbols[idx], f"Expected {expected_symbols[idx]}, got {stock_data['symbol']}"
        stock_values.append(stock_data["stock value"])


#test 5
def test_get_portfolio_value(stock_ids):
    """Execute a GET /portfolio-value. Let pv be the value of the “portfolio value” field returned. 
    The test is successful if 
    (i) the return status code is 200 
    (ii) pv*.97 <=sv1 + sv2 + sv3 <= pv*1.03"""
    response = requests.get(f"{BASE_URL}/portfolio-value")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    portfolio_data = response.json()
    pv = portfolio_data.get("portfolio value")

    stocks = [stock1, stock2, stock3]
    sv_total = 0
    for index, stock in enumerate(stocks):
        sv_total += requests.get(f"{BASE_URL}/stock-value/{stock_ids[index]}").json().get("stock value")

    lower_bound = pv * 0.97
    upper_bound = pv * 1.03
    assert lower_bound <= sv_total <= upper_bound, f"Stock values sum {sv_total} is outside the range [{lower_bound}, {upper_bound}] of portfolio value {pv}"


#test 6
def test_create_stock_missing_symbol():
    """Execute a POST /stocks request supplying the details of stock7.
    The test is successful if 
    (i) the return status code is 400"""
    response = requests.post(f"{BASE_URL}/stocks", json=stock7)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


#test 7
def test_delete_stock(stock_ids):
    """execute a DELETE /stocks/{ID} request, using the ID of stock2 (Apple Inc.). 
    The test is successful if the return status code is 204."""
    response = requests.delete(f"{BASE_URL}/stocks/{stock_ids[1]}")
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"


#test 8
def test_get_deleted_stock(stock_ids):
    """Perform a GET stocks/{ID} request, using the ID of stock2. 
    The test is successful if the return status code is 404."""
    response = requests.get(f"{BASE_URL}/stocks/{stock_ids[1]}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


#test 9
def test_create_stock_invalid_date_format():
    """Execute a POST / stocks request supplying the details of stock8. 
    The test is successful if the return status code is or 400 (purchase date is incorrect format)."""
    response = requests.post(f"{BASE_URL}/stocks", json=stock8)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"