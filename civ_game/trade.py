class TradeRoute:
    def __init__(self, origin_city, destination_city, resource, amount):
        self.origin_city = origin_city
        self.destination_city = destination_city
        self.resource = resource
        self.amount = amount
        self.is_active = True

    def update(self):
        if self.is_active:
            self.origin_city.owner.resources[self.resource] -= self.amount
            self.destination_city.owner.resources[self.resource] += self.amount