BUILDINGS = {
    "granary": {
        "name": "Granary",
        "cost": {"wood": 100},
        "requires_tech": "pottery",
        "effects": {
            "food_storage": 50, # Placeholder for now
            "food_per_turn": 2,
        },
        "description": "Increases food storage and provides +2 food per turn."
    },
    "library": {
        "name": "Library",
        "cost": {"wood": 150},
        "requires_tech": "writing",
        "effects": {
            "research_bonus": 0.1, # 10% bonus
        },
        "description": "Increases research points generation by 10% in this city."
    },
    "walls": {
        "name": "Walls",
        "cost": {"stone": 100}, # Let's introduce stone cost
        "requires_tech": "masonry",
        "effects": {
            "defense_bonus": 50, # Placeholder for combat
        },
        "description": "Provides a defensive bonus to the city."
    },
    "stock_exchange": {
        "name": "Stock Exchange",
        "cost": {"gold": 500},
        "requires_tech": "computers",
        "effects": {
            "gold_per_turn": 20,
        },
        "description": "Unlocks the financial market and generates significant gold."
    },
    "monument": {
        "name": "Monument",
        "cost": {"wood": 60},
        "requires_tech": None, # Available from the start
        "effects": {
            "culture_per_turn": 2,
        },
        "description": "A basic cultural building that generates culture points each turn."
    },
}