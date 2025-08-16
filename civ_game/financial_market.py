import random

class FinancialMarket:
    """
    A simplified simulation of a global stock market.
    Inspired by Black-Scholes principles (risk, volatility, growth).
    """
    def __init__(self):
        self.stock_price = 100.0
        self.volatility = 0.1 # Represents the risk (sigma)
        self.drift = 0.01 # Represents the risk-free interest rate (r)

    def update(self):
        """
        Updates the stock price for a new turn using a simplified geometric Brownian motion.
        """
        # Random shock (Brownian motion component)
        random_shock = random.uniform(-self.volatility, self.volatility)
        
        # Calculate the new price
        self.stock_price *= (1 + self.drift + random_shock)

        # Ensure price doesn't go below a certain threshold
        if self.stock_price < 10:
            self.stock_price = 10

    def get_price(self):
        return self.stock_price