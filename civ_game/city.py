from .buildings import BUILDINGS
from .units import UNITS

class City:
    """
    Represents a single city in the game.
    """
    def __init__(self, name, owner, location):
        self.name = name
        self.owner = owner  # The civilization that owns the city
        self.location = location  # A tuple (x, y)
        self.population = 100
        self.buildings = []
        self.production_points = 0
        self.current_production = None
        self.border_radius = 1

    def update(self):
        """
        Update the city's state for a new turn.
        """
        # 1. Generate production
        self.generate_production()

        # 2. Work on current production
        if self.current_production:
            item_key = self.current_production
            item_info = None
            item_type = None

            if item_key in BUILDINGS:
                item_info = BUILDINGS[item_key]
                item_type = "building"
            elif item_key in UNITS:
                item_info = UNITS[item_key]
                item_type = "unit"

            if item_info:
                cost_amount = list(item_info["cost"].values())[0] # Assuming single resource cost for now

                if self.production_points >= cost_amount:
                    self.production_points -= cost_amount
                    if item_type == "building":
                        self.buildings.append(item_key)
                        print(f"{self.name} has built a {item_info['name']}!")
                    elif item_type == "unit":
                        self.owner.add_unit(item_key)
                        print(f"{self.name} has trained a {item_info['name']}!")
                    self.current_production = None
        
        # Border expansion
        if self.owner.resources["culture"] > self.border_radius * 100:
            self.border_radius += 1

    def generate_production(self):
        """Generates production points each turn."""
        base_production = self.population // 15
        
        # Apply civilization trait bonus
        if "bonuses" in self.owner.traits and "production_bonus" in self.owner.traits["bonuses"]:
            base_production += self.owner.traits["bonuses"]["production_bonus"]

        self.production_points += base_production

    def get_food_bonus(self):
        """Calculates the total food bonus from buildings."""
        bonus = 0
        for building_key in self.buildings:
            effects = BUILDINGS[building_key]["effects"]
            if "food_per_turn" in effects:
                bonus += effects["food_per_turn"]
        return bonus

    def get_culture_bonus(self):
        """Calculates the total culture bonus from buildings."""
        bonus = 0
        for building_key in self.buildings:
            effects = BUILDINGS[building_key]["effects"]
            if "culture_per_turn" in effects:
                bonus += effects["culture_per_turn"]
        return bonus

    def get_research_bonus(self):
        """Calculates the total research bonus from buildings."""
        bonus = 1.0
        for building_key in self.buildings:
            effects = BUILDINGS[building_key]["effects"]
            if "research_bonus" in effects:
                bonus += effects["research_bonus"]
        return bonus

    def __str__(self):
        production_status = f", Prod: {self.current_production}" if self.current_production else ""
        return f"{self.name} (Pop: {self.population}{production_status})"