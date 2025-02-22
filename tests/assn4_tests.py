import pytest
import requests

BASE_URL = "http://localhost:5001"  # Adjust this to match your service's base URL

# Sample stock data
STOCKS = [
    {"name": "NVIDIA Corporation", "symbol": "NVDA", "purchase_price": 134.66, "purchase_date": "18-06-2024", "shares": 7},
    {"name": "Apple Inc.", "symbol": "AAPL", "purchase_price": 183.63, "purchase_date": "22-02-2024", "shares": 19},
    {"name": "Alphabet Inc.", "symbol": "GOOG", "purchase_price": 140.12, "purchase_date": "24-10-2024", "shares": 14}
]

@pytest.fixture(scope="module")
def stock_ids():
    """Fixture to store stock IDs after creation."""
    return []

@pytest.fixture(scope="module")
def stock_values():
    """Fixture to store stock values after creation."""
    return []

#  test 4
# @pytest.fixture(scope="module")
# def stock_values(stock_ids):
#     """Fixture to fetch and store stock values."""
#     expected_symbols = ["NVDA", "AAPL", "GOOG"]
#     stock_values_dict = {}
#
#     for idx, stock_id in enumerate(stock_ids):
#         response = requests.get(f"{BASE_URL}/stock-value/{stock_id}")
#         assert response.status_code == 200, f"Failed to get stock value for {expected_symbols[idx]}"
#
#         stock_data = response.json()
#         assert stock_data["symbol"] == expected_symbols[idx], f"Expected {expected_symbols[idx]}, got {stock_data['symbol']}"
#
#         stock_values_dict[expected_symbols[idx]] = stock_data["stock_value"]
#
#     return stock_values_dict  # { "NVDA": sv1, "AAPL": sv2, "GOOG": sv3 }


#test 1
def test_create_stocks(stock_ids):
    """Test POST /stock requests for creating stocks."""
    for stock in STOCKS:
        response = requests.post(f"{BASE_URL}/stocks", json=stock)
        assert response.status_code == 201
        stock_id = response.json().get("id")
        assert stock_id is not None
        stock_ids.append(stock_id)

    assert len(set(stock_ids)) == 3  # Ensure IDs are unique

#test 2
def test_get_stock(stock_ids):
    """Test GET /stocks/{ID} for a single stock."""
    stock_id = stock_ids[0]
    response = requests.get(f"{BASE_URL}/stocks/{stock_id}")
    assert response.status_code == 200
    assert response.json()["symbol"] == "NVDA"

# todo - check what the meaning of the test
#test 3
def test_get_all_stocks():
    response = requests.get(f"{BASE_URL}/stocks")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Ensure the response content type is JSON
    assert "application/json" in response.headers.get("Content-Type", ""), "Response is not JSON"

    # Validate JSON format and structure
    try:
        stocks = response.json()
        assert isinstance(stocks, list), "Response is not a list"
        assert len(stocks) == 3, f"Expected 3 stocks, got {len(stocks)}"
        for stock in stocks:
            assert isinstance(stock, dict), "Each stock should be a JSON object (dict)"
    except (ValueError, TypeError) as e:
        pytest.fail(f"Response is not valid JSON or structured incorrectly: {e}")

#test 4
def test_stock_values(stock_ids, stock_values):
    """Fixture to fetch and store stock values."""
    expected_symbols = ["NVDA", "AAPL", "GOOG"]

    for idx, stock_id in enumerate(stock_ids):
        response = requests.get(f"{BASE_URL}/stock-value/{stock_id}")
        assert response.status_code == 200, f"Failed to get stock value for {expected_symbols[idx]}"

        stock_data = response.json()
        assert stock_data["symbol"] == expected_symbols[idx], f"Expected {expected_symbols[idx]}, got {stock_data['symbol']}"

        stock_values.append(stock_data["stock value"])


#test 5
def test_get_portfolio_value(stock_values):
    response = requests.get(f"{BASE_URL}/portfolio-value")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    # Extract portfolio value
    portfolio_data = response.get("portfolio value")
    pv = portfolio_data.get("portfolio value")


    # Fetch individual stock values
    sv_total = 0
    stock_response = requests.get(f"{BASE_URL}/stocks")

    assert stock_response.status_code == 200, "Failed to retrieve stock data"
    for value in stock_values:
        sv_total += value
    # Check if sum of stock values is within 0.3% of portfolio value
    lower_bound = pv * 0.97
    upper_bound = pv * 1.03
    assert lower_bound <= sv_total <= upper_bound, f"Stock values sum {sv_total} is outside the range [{lower_bound}, {upper_bound}] of portfolio value {pv}"
