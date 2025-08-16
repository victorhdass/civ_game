import random

class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.history = [price]

    def update(self):
        self.price *= 1 + random.uniform(-0.05, 0.05)
        self.history.append(self.price)

class StockMarket:
    def __init__(self):
        self.stocks = [
            Stock("Food Co.", 100),
            Stock("Wood Inc.", 120),
            Stock("Stone & Sons", 80),
        ]

    def update(self):
        for stock in self.stocks:
            stock.update()