from PIL import Image

class World:
    """
    Represents the game world.
    """
    def __init__(self, size_x, size_y, game):
        self.game = game
        self.grid = self._generate_grid()
        self.size_x = len(self.grid)
        self.size_y = len(self.grid[0])
        self.roads = set()

    @property
    def width(self):
        return self.size_x

    @property
    def height(self):
        return self.size_y

    def _generate_grid(self):
        """
        Generates the world grid from the world_map.png image using Pillow.
        """
        try:
            image = Image.open('civ_game/world_map.png')
            width, height = image.size
            rgb_image = image.convert('RGB')
            
            grid = [["" for _ in range(height)] for _ in range(width)]
            
            for x in range(width):
                for y in range(height):
                    r, g, b = rgb_image.getpixel((x, y))
                    
                    if r == 0 and g == 0 and b == 0:  # Black for land
                        grid[x][y] = "grass"
                    else:  # White for water
                        grid[x][y] = "water"
            return grid
        except FileNotFoundError:
            # Fallback to a simple grid if the map image is not found
            width, height = 80, 40
            grid = [["" for _ in range(height)] for _ in range(width)]
            for x in range(width):
                for y in range(height):
                    if 20 <= x < 60 and 10 <= y < 30:
                        grid[x][y] = "grass"
                    else:
                        grid[x][y] = "water"
            return grid

    def update(self):
        """
        Update the world's state for a new turn.
        """
        # World logic will go here
        pass

    def expand_world(self, new_width, new_height):
        """Expands the world map to a new size."""
        print(f"The world has expanded! New size: {new_width}x{new_height}")
        old_width = self.size_x
        old_height = self.size_y
        self.size_x = new_width
        self.size_y = new_height

        new_grid = [["" for _ in range(new_height)] for _ in range(new_width)]

        for x in range(old_width):
            for y in range(old_height):
                new_grid[x][y] = self.grid[x][y]

        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        seed = random.randint(0, 100)

        for x in range(new_width):
            for y in range(new_height):
                if x >= old_width or y >= old_height:
                    value = noise.pnoise2(x / scale,
                                          y / scale,
                                          octaves=octaves,
                                          persistence=persistence,
                                          lacunarity=lacunarity,
                                          repeatx=new_width,
                                          repeaty=new_height,
                                          base=seed)
                    
                    value = (value + 1) / 2

                    if value < 0.5:
                        new_grid[x][y] = "water"
                    elif value < 0.7:
                        new_grid[x][y] = "grass"
                    elif value < 0.85:
                        new_grid[x][y] = "forest"
                    else:
                        new_grid[x][y] = "mountain"
        self.grid = new_grid

    def get_tile_owner(self, x, y):
        """Returns the civilization that owns the tile at (x, y), or None."""
        for civ in self.game.civilizations:
            for city in civ.cities:
                # Simple ownership rule: tile is owned by the closest city
                # (This can be expanded with more complex border logic)
                if abs(city.location[0] - x) <= 1 and abs(city.location[1] - y) <= 1:
                    return civ
        return None