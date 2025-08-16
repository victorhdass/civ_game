import pygame

class GUI:
    def __init__(self, game):
        self.game = game
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Civilization Game")
        self.zoom = 1.0
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.panning = False
        self.last_left_click_time = 0
        self.last_right_click_time = 0
        self.double_click_interval = 300  # milliseconds

    def draw_game_state(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        
        # Always draw the map
        self.draw_map(font)

        # Draw contextual screens on top
        if self.game.game_state == "CITY_VIEW":
            self.draw_city_view(font)
        elif self.game.game_state == "EMPIRE_VIEW":
            self.draw_empire_view(font)
        elif self.game.game_state == "SELECTING_PANTHEON":
            self.draw_pantheon_selection(font)
        else: # Normal view or other selection states
            self.draw_main_ui(font)

        self.draw_notifications(font)
        pygame.display.flip()

    def draw_map(self, font):
        tile_width = (self.screen_width / self.game.world.width) * self.zoom
        tile_height = (self.screen_height / self.game.world.height) * self.zoom
        
        terrain_colors = {
            "water": (0, 0, 255), "grass": (0, 255, 0),
            "forest": (0, 100, 0), "mountain": (139, 69, 19)
        }

        start_x = max(0, int(-self.camera_offset_x / tile_width))
        end_x = min(self.game.world.width, int((-self.camera_offset_x + self.screen_width) / tile_width) + 1)
        start_y = max(0, int(-self.camera_offset_y / tile_height))
        end_y = min(self.game.world.height, int((-self.camera_offset_y + self.screen_height) / tile_height) + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                terrain = self.game.world.grid[x][y]
                color = terrain_colors.get(terrain, (128, 128, 128))
                screen_x = self.camera_offset_x + x * tile_width
                screen_y = self.camera_offset_y + y * tile_height
                rect = pygame.Rect(screen_x, screen_y, tile_width, tile_height)
                pygame.draw.rect(self.screen, color, rect)

        # Draw all cities and borders
        for civ in self.game.civilizations:
            for city in civ.cities:
                x, y = city.location
                
                # Draw city center
                screen_x = self.camera_offset_x + x * tile_width
                screen_y = self.camera_offset_y + y * tile_height
                radius = int(tile_width / 4 + city.population / 50)
                pygame.draw.circle(self.screen, civ.color, (int(screen_x + tile_width / 2), int(screen_y + tile_height / 2)), radius, 0)

                # Draw borders for all cities
                border_radius_pixels = int(city.border_radius * tile_width)
                pygame.draw.circle(self.screen, (*civ.color, 50), (int(screen_x + tile_width / 2), int(screen_y + tile_height / 2)), border_radius_pixels, 0)
                pygame.draw.circle(self.screen, civ.color, (int(screen_x + tile_width / 2), int(screen_y + tile_height / 2)), border_radius_pixels, 1)

    def draw_main_ui(self, font):
        # Top-left info
        year = self.game.get_current_year()
        year_str = f"{abs(year)} {'BC' if year < 0 else 'AD'}"
        turn_text = font.render(f"Turn: {self.game.turn} ({year_str})", True, (255, 255, 255))
        self.screen.blit(turn_text, (10, 10))
        current_civ = self.game.get_current_civilization()
        civ_text = font.render(f"Civilization: {current_civ.name}", True, (255, 255, 255))
        self.screen.blit(civ_text, (10, 40))

        # Bottom menu
        # Horizontal Menu
        menu_y = self.screen.get_height() - 30
        menu_items = [
            "(1) Research", "(2) Policy", "(3) Found City",
            "(4) Army", "(5) Diplomacy", "(6) Great People", "(7) Save", "(8) End Turn",
            "(E) Empire"
        ]
        
        # Blinking notification for Empire View
        if self.game.turn % 10 == 0:
            empire_text = font.render("(E) Empire", True, (255, 255, 0))
            self.screen.blit(empire_text, (self.screen_width - 150, 10))
        
        # Draw a background for the menu
        menu_bg_rect = pygame.Rect(0, self.screen.get_height() - 40, self.screen.get_width(), 40)
        pygame.draw.rect(self.screen, (20, 20, 20), menu_bg_rect)

        x_offset = 10
        for item in menu_items:
            text = font.render(item, True, (255, 255, 255))
            self.screen.blit(text, (x_offset, menu_y))
            x_offset += text.get_width() + 20 # Add spacing
        
        # Contextual selection lists
        if self.game.game_state == "SELECTING_TECH": self.draw_tech_selection(font)
        elif self.game.game_state == "SELECTING_POLICY": self.draw_policy_selection(font)
        elif self.game.game_state == "SELECTING_CITY_PRODUCTION": self.draw_city_production_selection(font)
        elif self.game.game_state == "DIPLOMACY_SCREEN": self.draw_diplomacy_screen(font)
        elif self.game.game_state == "GREAT_PEOPLE_SCREEN": self.draw_great_people_screen(font)

    def draw_tech_selection(self, font):
        self.draw_selection_list("Select a Technology:", self.game.available_techs_for_selection,
                                 lambda item: f"{item[1]['name']} (Cost: {item[1]['cost']}) - {self.game.get_research_time(item[1]['cost'])} turns")

    def draw_policy_selection(self, font):
        self.draw_selection_list("Select an Economic Policy:", self.game.available_policies_for_selection,
                                 lambda item: item[1]['name'])

    def draw_city_production_selection(self, font):
        title = f"Select Production for {self.game.selected_city.name}:"
        self.draw_selection_list(title, self.game.producible_items_for_selection,
                                 lambda item: f"[{item[0].capitalize()}] {item[2]['name']}")

    def draw_diplomacy_screen(self, font):
        title = "Diplomacy - Select a Civilization:"
        self.draw_selection_list(title, self.game.diplomacy_civs_for_selection,
                                 lambda item: f"{item.name} (Status: {self.game.get_current_civilization().get_relation(item.name)})",
                                 ["Declare War", "Propose Peace", "Send Spy", "Create Trade Route"])

    def draw_great_people_screen(self, font):
        title = "Recruit a Great Person:"
        self.draw_selection_list(title, self.game.available_great_people_for_selection,
                                 lambda item: f"{item[1]['name']} ({item[1]['type']}) - Cost: {item[1]['cost']} GPP")
    
    def draw_pantheon_selection(self, font):
        self.draw_selection_list("Choose a Pantheon Belief:", self.game.available_pantheons_for_selection,
                                 lambda item: f"{item[1]['name']} - {item[1]['description']}")

    def draw_selection_list(self, title, items, formatter, actions=None):
        y_start = 100
        title_surf = pygame.font.Font(None, 30).render(title, True, (255, 255, 0))
        self.screen.blit(title_surf, (200, y_start))
        for i, item in enumerate(items):
            item_text = f"{i + 1}. {formatter(item)}"
            text_surf = pygame.font.Font(None, 30).render(item_text, True, (255, 255, 255))
            self.screen.blit(text_surf, (200, y_start + 40 + i * 35))
        
        if actions:
            y_start += len(items) * 35 + 20
            for i, action in enumerate(actions):
                action_text = f"  ({i + 1}) {action}"
                text_surf = pygame.font.Font(None, 30).render(action_text, True, (255, 255, 150))
                self.screen.blit(text_surf, (220, y_start + 40 + i * 25))

    def draw_city_view(self, font):
        self.draw_overlay()
        city = self.game.selected_city
        title = f"City of {city.name}"
        infos = [f"Population: {city.population}", "Buildings:"]
        if not city.buildings:
            infos.append("  None")
        else:
            for building_key in city.buildings:
                building_name = self.game.get_building_info(building_key).get('name', building_key)
                infos.append(f"  - {building_name}")
        
        infos.append("---")
        infos.append("Available Buildings:")
        
        available_buildings = self.game.get_available_buildings_for_city(city)
        if available_buildings:
            for i, (key, info) in enumerate(available_buildings):
                cost_str = ", ".join([f"{v} {k}" for k, v in info['cost'].items()])
                infos.append(f"  ({i + 1}) {info['name']} (Cost: {cost_str})")
        else:
            infos.append("  None")
        
        infos.append("---")
        infos.append("(B) Build Road (Cost: 10 gold)")

        self.draw_info_screen(title, infos, True)

    def draw_empire_view(self, font):
        self.draw_overlay()
        civ = self.game.get_current_civilization()
        title = f"The {civ.name} Empire"
        
        researching = "Nothing"
        if civ.current_research:
            researching = self.game.get_tech_info(civ.current_research).get('name', 'Unknown')
        
        policy = "None"
        if civ.current_policy:
            policy = self.game.get_policy_info(civ.current_policy).get('name', 'Unknown')

        infos = [
            f"Gold: {civ.resources['gold']} | Culture: {civ.resources['culture']} | Faith: {civ.resources['faith']}",
            f"Researching: {researching} ({civ.research_points} points)",
            f"Economic Policy: {policy}",
            f"Research Investment: {civ.research_investment}%",
            f"Inflation: {civ.inflation:.2f}%",
            f"Growth: {civ.get_growth_rate():.2f}%",
            "---",
            "Military:",
            "  Units: " + ", ".join([f"{v}x {self.game.get_unit_info(k).get('name', k)}" for k, v in civ.units.items()]) if civ.units else "  None",
            "---",
            "Cities:"
        ]
        for city in civ.cities:
            production = "Nothing"
            if city.current_production:
                item_type = "building" if "building" in city.current_production else "unit"
                item_info = self.game.get_building_info(city.current_production) if item_type == "building" else self.game.get_unit_info(city.current_production)
                production = item_info.get('name', city.current_production)
            infos.append(f"  - {city.name} (Pop: {city.population}) - Producing: {production}")
        self.draw_info_screen(title, infos)

    def draw_overlay(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

    def draw_info_screen(self, title, infos, city_view=False):
        title_font = pygame.font.Font(None, 50)
        font = pygame.font.Font(None, 30)
        
        title_surf = title_font.render(title, True, (255, 255, 0))
        self.screen.blit(title_surf, (self.screen_width // 2 - title_surf.get_width() // 2, 50))

        y_start = 150
        for i, info in enumerate(infos):
            info_surf = font.render(info, True, (255, 255, 255))
            self.screen.blit(info_surf, (100, y_start + i * 30))

        if city_view:
            action_text = font.render("Press the corresponding number to build.", True, (255, 255, 150))
            self.screen.blit(action_text, (100, self.screen_height - 80))

        if self.game.game_state == "EMPIRE_VIEW":
            action_text = font.render("Press '+' or '-' to adjust research investment.", True, (255, 255, 150))
            self.screen.blit(action_text, (100, self.screen_height - 80))

        esc_text = font.render("Press ESC to return", True, (255, 255, 0))
        self.screen.blit(esc_text, (self.screen_width // 2 - esc_text.get_width() // 2, self.screen_height - 50))

    def draw_notifications(self, font):
        for i, notification in enumerate(self.game.notifications):
            text_surface = font.render(notification['message'], True, (255, 255, 0))
            bg_rect = text_surface.get_rect(center=(self.screen_width // 2, 100 + i * 30))
            bg_rect.inflate_ip(10, 5)
            
            overlay = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, bg_rect.topleft)
            self.screen.blit(text_surface, text_surface.get_rect(center=bg_rect.center))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = "NORMAL"
                elif self.game.game_state == "NORMAL" and event.key == pygame.K_e:
                    self.game.game_state = "EMPIRE_VIEW"
                elif self.game.game_state == "EMPIRE_VIEW":
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.game.get_current_civilization().research_investment = min(100, self.game.get_current_civilization().research_investment + 10)
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.game.get_current_civilization().research_investment = max(0, self.game.get_current_civilization().research_investment - 10)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    self.game.handle_player_action(event.key - pygame.K_0)
                elif self.game.game_state == "CITY_VIEW" and event.key == pygame.K_b:
                    self.game.handle_city_view_action(11)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                if event.button == 1:  # Left mouse button
                    if current_time - self.last_left_click_time < self.double_click_interval:
                        self.zoom_at_point(event.pos, 1.5)
                    self.last_left_click_time = current_time
                    self.handle_map_click(event.pos)
                elif event.button == 3:  # Right mouse button
                    if current_time - self.last_right_click_time < self.double_click_interval:
                        self.zoom_at_point(event.pos, 1 / 1.5)
                    self.last_right_click_time = current_time
                elif event.button == 2:  # Middle mouse button for panning
                    self.panning = True
                    pygame.mouse.get_rel()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.panning = False

            elif event.type == pygame.MOUSEMOTION and self.panning:
                dx, dy = event.rel
                self.camera_offset_x += dx
                self.camera_offset_y += dy

    def zoom_at_point(self, mouse_pos, zoom_factor):
        tile_width = (self.screen_width / self.game.world.width) * self.zoom
        tile_height = (self.screen_height / self.game.world.height) * self.zoom

        world_x = (mouse_pos[0] - self.camera_offset_x) / tile_width
        world_y = (mouse_pos[1] - self.camera_offset_y) / tile_height

        new_zoom = self.zoom * zoom_factor
        self.zoom = max(0.2, min(new_zoom, 5.0))

        new_tile_width = (self.screen_width / self.game.world.width) * self.zoom
        new_tile_height = (self.screen_height / self.game.world.height) * self.zoom

        self.camera_offset_x = mouse_pos[0] - world_x * new_tile_width
        self.camera_offset_y = mouse_pos[1] - world_y * new_tile_height
    def handle_map_click(self, mouse_pos):
        tile_width = (self.screen_width / self.game.world.width) * self.zoom
        tile_height = (self.screen_height / self.game.world.height) * self.zoom
        
        world_x = (mouse_pos[0] - self.camera_offset_x) / tile_width
        world_y = (mouse_pos[1] - self.camera_offset_y) / tile_height
        
        clicked_x = int(world_x)
        clicked_y = int(world_y)

        player_civ = self.game.get_current_civilization()
        
        # Check if a city was clicked
        clicked_city = None
        for civ in self.game.civilizations:
            for city in civ.cities:
                if city.location == (clicked_x, clicked_y):
                    clicked_city = city
                    break
            if clicked_city:
                break

        if clicked_city:
            # Allow access only if the city belongs to the player
            if clicked_city.owner == player_civ:
                if self.game.game_state == "NORMAL":
                    self.game.enter_city_view(clicked_city)
                elif self.game.game_state == "SELECTING_CITY_FOR_PRODUCTION":
                    self.game.prepare_production_list_for_city(clicked_city)
            else:
                # Show basic info for foreign cities
                self.game.add_notification(f"This is {clicked_city.name}, population {clicked_city.population}.", 5)