EUREKAS = {
    "pottery": {
        "trigger_type": "resource",
        "resource": "food",
        "amount": 150,
        "description": "Have 150 food in your reserves.",
        "bonus": 0.5 # 50% research cost reduction
    },
    "masonry": {
        "trigger_type": "building",
        "building": "walls", # This is a bit circular, let's change it
        "description": "Build your first quarry (not yet implemented). For now, let's tie it to founding a second city.",
        "trigger_type": "city_count",
        "count": 2,
        "bonus": 0.5
    },
    "writing": {
        "trigger_type": "diplomacy",
        "action": "meet_civ",
        "count": 1,
        "description": "Meet another civilization.",
        "bonus": 0.5
    },
    # We can add more complex triggers later
}