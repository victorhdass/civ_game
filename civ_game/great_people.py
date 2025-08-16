GREAT_PEOPLE = {
    "ancient": {
        "requires_tech": None, # Available from the start
        "people": {
            "homer": {
                "name": "Homer",
                "type": "Artist",
                "cost": 100,
                "effect": {"type": "culture_bomb", "amount": 50},
                "description": "Instantly provides a large amount of culture."
            },
            "sun_tzu": {
                "name": "Sun Tzu",
                "type": "General",
                "cost": 100,
                "civ_affinity": "Japanese", # Example of affinity
                "effect": {"type": "unit_xp_boost"},
                "description": "Provides a combat bonus to nearby units (not yet implemented)."
            },
        }
    },
    "classical": {
        "requires_tech": "writing",
        "people": {
            "hypatia": {
                "name": "Hypatia",
                "type": "Scientist",
                "cost": 200,
                "effect": {"type": "free_tech"},
                "description": "Grants a free technology."
            },
        }
    },
    "modern": {
        "requires_tech": "computers",
        "people": {
            "alan_turing": {
                "name": "Alan Turing",
                "type": "Scientist",
                "cost": 1000,
                "effect": {"type": "research_boost", "amount": 0.5, "duration": 10},
                "description": "Boosts research by 50% for 10 turns."
            },
        }
    },
}