POLICIES = {
    "agrarianism": {
        "name": "Agrarianism",
        "description": "Focus on agriculture, increasing food production by 20% but decreasing wood production by 10%.",
        "requires_tech": "agriculture",
        "effects": {
            "food_bonus": 0.2,
            "wood_bonus": -0.1,
        }
    },
    "mercantilism": {
        "name": "Mercantilism",
        "description": "Focus on trade and commerce, increasing wood production by 20% but decreasing food production by 10%.",
        "requires_tech": "writing",
        "effects": {
            "wood_bonus": 0.2,
            "food_bonus": -0.1,
        }
    },
    "militarism": {
        "name": "Militarism",
        "description": "Focus on military, no immediate economic effect, but will be required for advanced units.",
        "requires_tech": "mining",
        "effects": {}
    },
    "feudalism": {
        "name": "Feudalism",
        "description": "A medieval policy that improves resource yields from worked tiles but reduces overall commerce.",
        "requires_tech": "masonry", # Placeholder, we'll need more techs later
        "effects": {}
    },
    "communism": {
        "name": "Communism",
        "description": "A modern era policy that greatly boosts industrial production but can lead to unrest.",
        "requires_tech": "alphabet", # Placeholder, we'll need more techs later
        "effects": {}
    },
}