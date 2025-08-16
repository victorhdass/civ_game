import random
from .technology import TECHNOLOGIES
from .policy import POLICIES
from .city import City
from .buildings import BUILDINGS
from .units import UNITS
from .city_names import CITY_NAMES
from .civilization_traits import CIVILIZATION_TRAITS
from .eureka import EUREKAS
from .trade import TradeRoute
from .religion import Religion, BELIEFS
from .map_data import CIVILIZATION_START_LOCATIONS

class Civilization:
    """
    Represents a single civilization in the game.
    """
    def __init__(self, name, difficulty="Normal", is_player=False):
        self.name = name
        self.difficulty = difficulty
        self.is_player = is_player
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.traits = CIVILIZATION_TRAITS.get(name, {})
        self.city_names = CITY_NAMES.get(name, [f"City {i+1}" for i in range(20)])
        self.cities = []
        # Start with a capital, ensuring it's on a land tile
        self.resources = {"food": 100, "wood": 100, "stone": 0, "gold": 50, "culture": 0, "faith": 0}

        if not self.is_player:
            if self.difficulty == "Hard":
                self.resources["gold"] += 100
                self.resources["culture"] += 20
            elif self.difficulty == "Normal":
                self.resources["gold"] += 50
        self.religion = None
        self.pantheon = None
        
        self.unlocked_technologies = []
        if "start_tech" in self.traits:
            self.unlocked_technologies.append(self.traits["start_tech"])

        self.research_points = 0
        self.research_investment = 100 # Default to 100%
        self.current_research = None
        self.current_policy = None
        self.units = []
        self.relations = {}
        self.triggered_eurekas = set()
        self.trade_routes = []
        self.great_person_points = 0
        self.recruited_great_people = []
        self.revealed_tiles = set()
        self.units = []
        self.inflation = 0.0

    def found_first_city(self, world):
        """Founds the first city in its historical start location."""
        if self.name in CIVILIZATION_START_LOCATIONS:
            x, y = CIVILIZATION_START_LOCATIONS[self.name]
            
            # Find the nearest valid land tile if the start location is in water
            if world.grid[x][y] == "water":
                closest_land = None
                min_dist = float('inf')
                for lx in range(world.width):
                    for ly in range(world.height):
                        if world.grid[lx][ly] not in ["water", "mountain"]:
                            dist = (lx - x)**2 + (ly - y)**2
                            if dist < min_dist:
                                min_dist = dist
                                closest_land = (lx, ly)
                if closest_land:
                    x, y = closest_land

            city_name = self.get_next_city_name()
            self.cities.append(City(city_name, self, (x, y)))
            self.reveal_tiles_around(x, y)
        else:
            # Fallback for civilizations without a defined start location
            valid_locations = []
            for x in range(world.width):
                for y in range(world.height):
                    if world.grid[x][y] not in ["water", "mountain"]:
                        valid_locations.append((x,y))
            if valid_locations:
                x, y = random.choice(valid_locations)
                city_name = self.get_next_city_name()
                self.cities.append(City(city_name, self, (x, y)))
                self.reveal_tiles_around(x, y)

    def update_ai(self, game):
        """
        Handles the decision-making for an AI-controlled civilization.
        """
        if not self.current_research:
            available_techs = []
            for tech_key, tech_info in TECHNOLOGIES.items():
                if tech_key not in self.unlocked_technologies:
                    requirements_met = True
                    if "requires" in tech_info:
                        for req in tech_info["requires"]:
                            if req not in self.unlocked_technologies:
                                requirements_met = False
                                break
                    if requirements_met:
                        available_techs.append(tech_key)
            if available_techs:
                if self.difficulty == "Hard":
                    available_techs.sort(key=lambda t: TECHNOLOGIES[t]['cost'])
                    self.current_research = available_techs[0]
                else:
                    self.current_research = random.choice(available_techs)
                game.add_notification(f"AI {self.name} started researching {self.current_research}", duration=3)

        for city in self.cities:
            if not city.current_production:
                producible_items = []
                for key, info in BUILDINGS.items():
                    if key not in city.buildings and info["requires_tech"] in self.unlocked_technologies:
                        producible_items.append(key)
                for key, info in UNITS.items():
                    if info["requires_tech"] is None or info["requires_tech"] in self.unlocked_technologies:
                        producible_items.append(key)
                if producible_items:
                    city.current_production = random.choice(producible_items)
                    game.add_notification(f"AI {city.name} started producing {city.current_production}", duration=3)

    @property
    def population(self):
        return sum(city.population for city in self.cities)

    @property
    def military_strength(self):
        return sum(UNITS[unit_key]["combat_strength"] for unit_key in self.units)

    def add_unit(self, unit_key):
        self.units.append(unit_key)

    def get_relation(self, other_civ_name):
        return self.relations.get(other_civ_name, "Neutral")

    def set_relation(self, other_civ_name, status):
        self.relations[other_civ_name] = status

    def update(self):
        self.update_visibility()
        for city in self.cities:
            city.update()
        
        food_consumed = self.population // 10
        self.resources["food"] -= food_consumed

        if self.resources["food"] > 0:
            growth = self.resources["food"] // 20
            if self.cities: self.cities[0].population += growth
        else:
            decline = self.resources["food"] // 5
            if self.cities: self.cities[0].population += decline

        for city in self.cities:
            if city.population < 0: city.population = 0
        
        self.gather_resources()
        self.generate_research()
        self.pay_maintenance()
        self.generate_great_person_points()
        self.generate_faith()

    def pay_maintenance(self):
        unit_maintenance = len(self.units) * 1
        building_maintenance = sum(len(city.buildings) for city in self.cities) * 2
        self.resources["gold"] -= (unit_maintenance + building_maintenance)

    def generate_great_person_points(self):
        self.great_person_points += self.resources["culture"]
        if self.pantheon and BELIEFS["pantheon"][self.pantheon]["effect"]["type"] == "great_person_points":
            self.great_person_points += BELIEFS["pantheon"][self.pantheon]["effect"]["amount"]

    def generate_faith(self):
        self.resources["faith"] += len(self.cities)

    def gather_resources(self):
        food = 5 * len(self.cities)
        wood = 2 * len(self.cities)
        gold = 1 * len(self.cities) + self.population // 5
        culture = 0

        if self.pantheon and BELIEFS["pantheon"][self.pantheon]["effect"]["type"] == "yield":
            if BELIEFS["pantheon"][self.pantheon]["effect"]["yield"] == "culture":
                culture += BELIEFS["pantheon"][self.pantheon]["effect"]["amount"]

        for route in self.trade_routes:
            if route.is_active: gold += route.base_yield

        for city in self.cities:
            food += city.get_food_bonus()
            culture += city.get_culture_bonus()

        if self.current_policy:
            effects = POLICIES[self.current_policy]["effects"]
            if "food_bonus" in effects: food *= (1 + effects["food_bonus"])
            if "wood_bonus" in effects: wood *= (1 + effects["wood_bonus"])

        # Cobb-Douglas production function
        capital = sum(len(city.buildings) for city in self.cities) + 1
        labor = self.population + 1
        production = int(10 * (capital**0.4) * (labor**0.6))

        self.resources["food"] += int(food)
        self.resources["wood"] += int(wood)
        self.resources["gold"] += int(gold) + production // 10
        self.resources["culture"] += int(culture)

    def generate_research(self):
        if self.population > 0:
            base_research = self.population // 20
            bonus = sum(city.get_research_bonus() - 1.0 for city in self.cities)
            if "bonuses" in self.traits and "research_bonus" in self.traits["bonuses"]:
                bonus += self.traits["bonuses"]["research_bonus"]
            
            final_research = int(base_research * (1 + bonus) * (self.research_investment / 100))
            self.research_points += max(1, final_research)

            if self.current_research:
                tech_key = self.current_research
                tech_info = TECHNOLOGIES[tech_key]
                cost = tech_info["cost"] * (1 - EUREKAS[tech_key]["bonus"]) if tech_key in self.triggered_eurekas else tech_info["cost"]
                
                if self.research_points >= cost:
                    self.research_points -= cost
                    self.unlocked_technologies.append(tech_key)
                    print(f"{self.name} has researched {tech_info['name']}!") # Keep for now
                    self.current_research = None

    def get_next_city_name(self):
        used_names = {city.name for city in self.cities}
        for name in self.city_names:
            if name not in used_names:
                return name
        return f"City {len(self.cities) + 1}"

    def reveal_tiles_around(self, x, y):
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                nx, ny = x + dx, y + dy
                self.revealed_tiles.add((nx, ny))

    def is_tile_visible(self, x, y):
        return (x, y) in self.revealed_tiles

    def update_visibility(self):
        self.revealed_tiles.clear()
        for city in self.cities:
            self.reveal_tiles_around(city.location[0], city.location[1])
        # Add unit visibility here later

    def get_growth_rate(self):
        return self.resources["food"] / (self.population + 1) * 100

    def create_trade_route(self, origin_city, destination_city, resource, amount):
        if self.resources[resource] >= amount:
            self.trade_routes.append(TradeRoute(origin_city, destination_city, resource, amount))
            return True
        return False