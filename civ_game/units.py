UNITS = {
    "warrior": {
        "name": "Warrior",
        "cost": {"production": 40},
        "requires_tech": None, # Available from the start
        "combat_strength": 10,
        "description": "A basic melee unit of the ancient era."
    },
    "archer": {
        "name": "Archer",
        "cost": {"production": 60},
        "requires_tech": "agriculture", # Placeholder tech
        "combat_strength": 12,
        "description": "A ranged unit effective for defense."
    },
    "swordsman": {
        "name": "Swordsman",
        "cost": {"production": 80},
        "requires_tech": "mining", # Placeholder tech
        "combat_strength": 15,
        "description": "A stronger melee unit that requires iron working."
    },
    "spy": {
        "name": "Spy",
        "cost": {"production": 100},
        "requires_tech": "writing",
        "combat_strength": 0,
        "description": "A covert unit used for espionage and intelligence gathering."
    },
}