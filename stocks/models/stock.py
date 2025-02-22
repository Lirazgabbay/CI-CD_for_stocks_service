"""
    stocks.py - Stock class defines the structure of a stock object and its methods.
"""
from validators import validate_date

class Stock:
    def __init__(self, symbol: str, purchase_price: float, shares: int,
                 purchase_date: str = 'NA', name: str = 'NA'):
        
        self.name = name
        self.symbol = symbol.upper()  
        self.purchase_price = round(purchase_price, 2)

        self.purchase_date = validate_date(purchase_date) if purchase_date != 'NA' else 'NA'
        self.shares = shares


    def to_dict(self):
        """Convert the Stock object to a dictionary."""
        return {
            "name": self.name,
            "symbol": self.symbol,
            "purchase price": self.purchase_price,
            "purchase date": self.purchase_date,
            "shares": self.shares
        }
    