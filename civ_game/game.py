from .world import World
from .civilization import Civilization
from .technology import TECHNOLOGIES
from .policy import POLICIES
from .city import City
from .buildings import BUILDINGS
from .units import UNITS
from .eureka import EUREKAS
from .trade import TradeRoute
from .great_people import GREAT_PEOPLE
from .religion import BELIEFS
import random
import pickle
import pygame
from .gui import GUI
from .stock_market import StockMarket

class Game:
    def __init__(self, civ_names, difficulty="Normal"):
        pygame.init()
        self.running = True
        self.gui = GUI(self)
        self.turn = 1
        self.difficulty = difficulty
        self.game_state = "NORMAL"
        self.player_turn = True
        
        self.available_techs_for_selection = []
        self.available_policies_for_selection = []
        self.producible_items_for_selection = []
        self.diplomacy_civs_for_selection = []
        self.available_great_people_for_selection = []
        self.available_pantheons_for_selection = []
        self.selected_city = None
        self.notifications = []
        
        self.world = World(None, None, self)
        self.civilizations = []
        for i, name in enumerate(civ_names):
            is_player = (i == 0)
            civ = Civilization(name, self.difficulty, is_player)
            civ.found_first_city(self.world)
            self.civilizations.append(civ)

    def run(self):
        while self.running:
            self.gui.handle_input()
            self.gui.draw_game_state()
            self.update_notifications()

            if not self.player_turn:
                self.run_ai_turns()
                self.player_turn = True
                self.add_notification(f"--- Your Turn ({self.turn}) ---", duration=3)
                self.check_pantheon_founding()

            pygame.time.wait(16)

    def check_pantheon_founding(self):
        player_civ = self.get_current_civilization()
        if not player_civ.pantheon and player_civ.resources["faith"] >= 25:
            self.prepare_pantheon_selection()

    def prepare_pantheon_selection(self):
        player_civ = self.get_current_civilization()
        if player_civ.pantheon: return
        self.available_pantheons_for_selection = list(BELIEFS["pantheon"].items())
        if self.available_pantheons_for_selection:
            self.game_state = "SELECTING_PANTHEON"
            self.add_notification("You have enough Faith to found a Pantheon!")

    def research_technology(self):
        civ = self.get_current_civilization()
        if civ.current_research:
            self.add_notification(f"Already researching {TECHNOLOGIES[civ.current_research]['name']}.")
            return
        self.available_techs_for_selection = []
        for tech_key, tech_info in TECHNOLOGIES.items():
            if tech_key not in civ.unlocked_technologies:
                req_met = all(req in civ.unlocked_technologies for req in tech_info.get("requires", []))
                if req_met:
                    self.available_techs_for_selection.append((tech_key, tech_info))
        if self.available_techs_for_selection:
            self.game_state = "SELECTING_TECH"
        else:
            self.add_notification("No new technologies available")

    def set_economic_policy(self):
        civ = self.get_current_civilization()
        self.available_policies_for_selection = []
        for key, info in POLICIES.items():
            if info.get("requires_tech") in civ.unlocked_technologies or not info.get("requires_tech"):
                self.available_policies_for_selection.append((key, info))
        if self.available_policies_for_selection:
            self.game_state = "SELECTING_POLICY"
        else:
            self.add_notification("No new policies available")

    def found_new_city(self):
        civ = self.get_current_civilization()
        if civ.resources["gold"] < 100:
            self.add_notification("You need at least 100 gold to found a new city.")
            return

        valid_locations = []
        for city in civ.cities:
            for dx in range(-city.border_radius, city.border_radius + 1):
                for dy in range(-city.border_radius, city.border_radius + 1):
                    if dx**2 + dy**2 > city.border_radius**2:
                        continue
                    nx, ny = city.location[0] + dx, city.location[1] + dy
                    if 0 <= nx < self.world.width and 0 <= ny < self.world.height:
                        if self.world.grid[nx][ny] not in ["water", "mountain"]:
                            if not any(c.location == (nx, ny) for c_civ in self.civilizations for c in c_civ.cities):
                                valid_locations.append((nx, ny))
        
        if valid_locations:
            x, y = random.choice(valid_locations)
            civ.cities.append(City(civ.get_next_city_name(), civ, (x, y)))
            civ.resources["gold"] -= 100
            civ.reveal_tiles_around(x, y)
            self.add_notification(f"Founded a new city at ({x}, {y})!")
            self.end_turn()
        else:
            self.add_notification("No valid location to found a new city.")

    def set_city_production(self):
        if not self.get_current_civilization().cities:
            self.add_notification("You have no cities.")
            return
        self.game_state = "SELECTING_CITY_FOR_PRODUCTION"
        self.add_notification("Click on a city to set its production.")

    def prepare_production_list_for_city(self, city):
        if city.current_production:
            self.add_notification(f"{city.name} is already producing.")
            self.game_state = "NORMAL"
            return
        self.selected_city = city
        civ = self.get_current_civilization()
        self.producible_items_for_selection = []
        for key, info in BUILDINGS.items():
            if key not in city.buildings and info.get("requires_tech") in civ.unlocked_technologies:
                self.producible_items_for_selection.append(("building", key, info))
        for key, info in UNITS.items():
            if info.get("requires_tech") is None or info.get("requires_tech") in civ.unlocked_technologies:
                self.producible_items_for_selection.append(("unit", key, info))
        if self.producible_items_for_selection:
            self.game_state = "SELECTING_CITY_PRODUCTION"
        else:
            self.add_notification("Nothing available to produce in this city.")
            self.game_state = "NORMAL"

    def view_army_and_wage_war(self):
        civ = self.get_current_civilization()
        army_info = "Your Army: " + (", ".join([f"{v}x {UNITS[k]['name']}" for k, v in civ.units.items()]) if civ.units else "None")
        self.add_notification(army_info)

    def diplomacy_screen(self):
        self.diplomacy_civs_for_selection = [c for c in self.civilizations if not c.is_player]
        if self.diplomacy_civs_for_selection:
            self.game_state = "DIPLOMACY_SCREEN"
        else:
            self.add_notification("No other civilizations to interact with.")

    def great_people_screen(self):
        civ = self.get_current_civilization()
        self.available_great_people_for_selection = []
        for era, data in GREAT_PEOPLE.items():
            if data.get("requires_tech") is None or data.get("requires_tech") in civ.unlocked_technologies:
                for key, info in data["people"].items():
                    if key not in civ.recruited_great_people:
                        self.available_great_people_for_selection.append((key, info))
        if self.available_great_people_for_selection:
            self.game_state = "GREAT_PEOPLE_SCREEN"
        else:
            self.add_notification("No Great People available.")

    def save_game(self):
        """Saves the current game state to a file."""
        try:
            with open("savegame.pkl", "wb") as f:
                pickle.dump(self, f)
            self.add_notification("Game saved successfully!")
        except Exception as e:
            self.add_notification(f"Error saving game: {e}")

    def get_current_civilization(self):
        return self.civilizations[0]

    def get_current_year(self):
        if self.turn < 100:
            return 4000 - (self.turn * 40)
        elif self.turn < 200:
            return 0 + ((self.turn - 100) * 10)
        else:
            return 1000 + ((self.turn - 200) * 5)

    def handle_player_action(self, choice):
        if not self.player_turn and self.game_state == "NORMAL": return

        if self.game_state == "NORMAL":
            actions = {1: self.research_technology, 2: self.set_economic_policy, 3: self.found_new_city,
                       4: self.view_army_and_wage_war, 5: self.diplomacy_screen,
                       6: self.great_people_screen, 7: self.save_game, 8: self.end_turn}
            if choice in actions: actions[choice]()
        
        elif self.game_state == "SELECTING_TECH": self.select_technology(choice)
        elif self.game_state == "SELECTING_POLICY": self.select_policy(choice)
        elif self.game_state == "SELECTING_CITY_PRODUCTION": self.select_city_production(choice)
        elif self.game_state == "DIPLOMACY_SCREEN": self.select_diplomacy_civ(choice)
        elif self.game_state == "DIPLOMACY_ACTION": self.handle_diplomacy_action(choice)
        elif self.game_state == "GREAT_PEOPLE_SCREEN": self.select_great_person(choice)
        elif self.game_state == "SELECTING_PANTHEON": self.select_pantheon(choice)
        elif self.game_state == "CITY_VIEW": self.handle_city_view_action(choice)

    def select_technology(self, choice):
        if 1 <= choice <= len(self.available_techs_for_selection):
            key, info = self.available_techs_for_selection[choice - 1]
            self.get_current_civilization().current_research = key
            self.add_notification(f"Started researching {info['name']}.")
            self.game_state = "NORMAL"
            self.end_turn()
        else:
            self.add_notification("Invalid choice.")
            self.game_state = "NORMAL"

    def select_policy(self, choice):
        if 1 <= choice <= len(self.available_policies_for_selection):
            key, info = self.available_policies_for_selection[choice - 1]
            self.get_current_civilization().current_policy = key
            self.add_notification(f"Enacted {info['name']}.")
            self.game_state = "NORMAL"
            self.end_turn()
        else:
            self.add_notification("Invalid choice.")
            self.game_state = "NORMAL"

    def select_city_production(self, choice):
        if 1 <= choice <= len(self.producible_items_for_selection):
            item_type, key, info = self.producible_items_for_selection[choice - 1]
            self.selected_city.current_production = key
            self.add_notification(f"{self.selected_city.name} is producing {info['name']}.")
            self.game_state = "NORMAL"
            self.end_turn()
        else:
            self.add_notification("Invalid choice.")
            self.game_state = "NORMAL"

    def select_diplomacy_civ(self, choice):
        if 1 <= choice <= len(self.diplomacy_civs_for_selection):
            self.selected_civ_for_diplomacy = self.diplomacy_civs_for_selection[choice - 1]
            self.game_state = "DIPLOMACY_ACTION"
            self.add_notification(f"Selected {self.selected_civ_for_diplomacy.name}. Choose an action.")
        else:
            self.add_notification("Invalid choice.")
            self.game_state = "NORMAL"

    def handle_diplomacy_action(self, choice):
        target_civ = self.selected_civ_for_diplomacy
        player_civ = self.get_current_civilization()
        if choice == 1: # Declare War
            player_civ.set_relation(target_civ.name, "War")
            target_civ.set_relation(player_civ.name, "War")
            self.add_notification(f"Declared war on {target_civ.name}!")
        elif choice == 2: # Propose Peace
            self.propose_peace(player_civ, target_civ)
        elif choice == 3: # Send Spy
            if target_civ.cities:
                self.send_spy(random.choice(target_civ.cities))
            else:
                self.add_notification(f"{target_civ.name} has no cities to spy on.")
        
        self.game_state = "NORMAL"
        self.end_turn()

    def propose_peace(self, proposer, recipient):
        if proposer.get_relation(recipient.name) != "War":
            self.add_notification("You are not at war with this civilization.")
            return

        # AI logic for accepting/rejecting peace
        if recipient.is_player: # Should not happen in current setup
            self.add_notification(f"{proposer.name} proposes peace.")
        else:
            # Simple AI logic: 50% chance to accept
            if random.random() < 0.5:
                proposer.set_relation(recipient.name, "Peace")
                recipient.set_relation(proposer.name, "Peace")
                self.add_notification(f"{recipient.name} has accepted your peace proposal.")
            else:
                self.add_notification(f"{recipient.name} has rejected your peace proposal.")

    def select_great_person(self, choice):
        if 1 <= choice <= len(self.available_great_people_for_selection):
            key, info = self.available_great_people_for_selection[choice - 1]
            player_civ = self.get_current_civilization()
            if player_civ.great_person_points >= info["cost"]:
                player_civ.great_person_points -= info["cost"]
                player_civ.recruited_great_people.append(key)
                self.add_notification(f"Recruited {info['name']}!")
            else:
                self.add_notification("Not enough Great Person Points.")
            self.game_state = "NORMAL"
            self.end_turn()
        else:
            self.add_notification("Invalid choice.")
            self.game_state = "NORMAL"

    def select_pantheon(self, choice):
        if 1 <= choice <= len(self.available_pantheons_for_selection):
            key, info = self.available_pantheons_for_selection[choice - 1]
            player_civ = self.get_current_civilization()
            player_civ.pantheon = key
            self.add_notification(f"Founded Pantheon: {info['name']}.")
            self.game_state = "NORMAL"
        else:
            self.add_notification("Invalid choice.")

    def get_research_time(self, cost):
        civ = self.get_current_civilization()
        research_per_turn = civ.population // 20 + 1
        return max(1, cost // research_per_turn)

    def send_spy(self, target_city):
        player_civ = self.get_current_civilization()
        if "spy" not in player_civ.units:
            self.add_notification("You have no spies to send.")
            return

        # Simple success/failure logic
        if random.random() < 0.7: # 70% chance of success
            self.add_notification(f"Spy successfully infiltrated {target_city.name}.")
            self.enter_city_view(target_city)
        else:
            self.add_notification(f"Your spy was caught trying to infiltrate {target_city.name}!")
            player_civ.units.remove("spy")
            self.game_state = "NORMAL"

    def end_turn(self):
        if not self.player_turn: return
        self.notifications.clear()
        self.get_current_civilization().update()
        self.turn += 1
        self.player_turn = False

    def run_ai_turns(self):
        self.add_notification("AI is taking its turn...", duration=1)
        for civ in self.civilizations:
            if not civ.is_player:
                civ.update()
                civ.update_ai(self)
    def view_city(self):
        self.game_state = "SELECTING_CITY_TO_VIEW"
        self.add_notification("Click on any city to view it.")

    def enter_city_view(self, city):
        self.selected_city = city
        self.game_state = "CITY_VIEW"

    def get_building_info(self, key): return BUILDINGS.get(key, {})
    def get_tech_info(self, key): return TECHNOLOGIES.get(key, {})
    def get_policy_info(self, key): return POLICIES.get(key, {})
    def get_unit_info(self, key): return UNITS.get(key, {})

    def get_available_buildings_for_city(self, city):
        available_buildings = []
        civ = city.owner
        for key, info in BUILDINGS.items():
            if key not in city.buildings and info.get("requires_tech") in civ.unlocked_technologies:
                available_buildings.append((key, info))
        return available_buildings

    def build_building(self, city, building_key):
        civ = city.owner
        building_info = BUILDINGS[building_key]
        cost = building_info["cost"]
        if civ.resources["gold"] >= cost.get("gold", 0) and civ.resources["wood"] >= cost.get("wood", 0) and civ.resources["stone"] >= cost.get("stone", 0):
            civ.resources["gold"] -= cost.get("gold", 0)
            civ.resources["wood"] -= cost.get("wood", 0)
            civ.resources["stone"] -= cost.get("stone", 0)
            city.buildings.append(building_key)
            self.add_notification(f"Built {building_info['name']} in {city.name}.")
        else:
            self.add_notification("Not enough resources to build.")

    def handle_city_view_action(self, choice):
        if choice == 11: # 'B' key
            self.build_road(self.selected_city)
        else:
            available_buildings = self.get_available_buildings_for_city(self.selected_city)
            if 1 <= choice <= len(available_buildings):
                building_key, _ = available_buildings[choice - 1]
                self.build_building(self.selected_city, building_key)
            else:
                self.add_notification("Invalid choice.")

    def build_road(self, city):
        civ = city.owner
        if civ.resources["gold"] < 10:
            self.add_notification("Not enough gold to build a road.")
            return

        # Simple road building logic: connect to the nearest city
        if len(civ.cities) > 1:
            other_cities = [c for c in civ.cities if c != city]
            other_cities.sort(key=lambda c: abs(c.location[0] - city.location[0]) + abs(c.location[1] - city.location[1]))
            target_city = other_cities[0]
            
            x1, y1 = city.location
            x2, y2 = target_city.location
            
            # Bresenham's line algorithm to draw a road
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                self.world.roads.add((x1, y1))
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy
            
            civ.resources["gold"] -= 10
            self.add_notification(f"Built a road between {city.name} and {target_city.name}.")
        else:
            self.add_notification("You need at least two cities to build a road.")

    def add_notification(self, message, duration=4):
        self.notifications.append({"message": message, "duration": duration * 60})

    def update_notifications(self):
        for n in self.notifications[:]:
            n['duration'] -= 1
            if n['duration'] <= 0:
                self.notifications.remove(n)
