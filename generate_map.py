from PIL import Image, ImageDraw

# Define the size of the map image
width, height = 400, 200
bg_color = (255, 255, 255)  # White for water
land_color = (0, 0, 0)  # Black for land

# Create a new image with a white background
image = Image.new("RGB", (width, height), bg_color)
draw = ImageDraw.Draw(image)

# Define the polygons for the continents (very simplified)
continents = [
    # North America
    [(50, 25), (60, 20), (125, 20), (150, 75), (100, 100), (75, 75)],
    # South America
    [(125, 110), (150, 125), (140, 175), (110, 160)],
    # Europe
    [(190, 25), (225, 25), (225, 60), (200, 75), (190, 50)],
    # Asia
    [(230, 25), (325, 25), (350, 75), (300, 100), (250, 75)],
    # Africa
    [(200, 90), (240, 90), (225, 150), (190, 140)],
    # Australia
    [(325, 150), (350, 140), (360, 160), (340, 175)],
]

# Draw each continent on the image
for continent in continents:
    draw.polygon(continent, fill=land_color)

# Save the image to a file
image.save("civ_game/world_map.png")

print("World map image generated successfully.")