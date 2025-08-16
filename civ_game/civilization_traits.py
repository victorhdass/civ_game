CIVILIZATION_TRAITS = {
    "Romans": {
        "name": "Romans",
        "description": "A disciplined and expansionist civilization. Their legions are formidable in the early game.",
        "advantages": [
            "+1 production in all cities.",
            "Start with the 'Mining' technology.",
            "Unique Unit: Legion (replaces Swordsman)."
        ],
        "disadvantages": [
            "-10% research speed."
        ],
        "unique_unit": "legion", # This will replace 'swordsman'
        "start_tech": "mining",
        "bonuses": {
            "production_bonus": 1,
            "research_bonus": -0.1,
        }
    },
    "Japanese": {
        "name": "Japanese",
        "description": "A culturally rich and resilient civilization. Their warriors fight with fierce determination.",
        "advantages": [
            "Units fight at full strength even when damaged (not yet implemented).",
            "Start with the 'Writing' technology.",
            "Unique Unit: Samurai (replaces Swordsman)."
        ],
        "disadvantages": [
            "Buildings cost 10% more wood."
        ],
        "unique_unit": "samurai", # This will replace 'swordsman'
        "start_tech": "writing",
        "bonuses": {
            "building_cost_modifier": 1.1,
        }
    },
    "Egyptians": {
        "name": "Egyptians",
        "description": "A civilization renowned for its monumental architecture and mastery of the river.",
        "advantages": [
            "+20% production towards wonders.",
            "Start with 'Pottery' technology."
        ],
        "disadvantages": [
            "Units have -1 movement in forest terrain."
        ],
        "start_tech": "pottery",
        "bonuses": {
            "wonder_production_modifier": 1.2,
        }
    },
    "Greeks": {
        "name": "Greeks",
        "description": "A cradle of philosophy and democracy, with a strong cultural and military tradition.",
        "advantages": [
            "Receive an extra economic policy slot.",
            "Start with 'Bronze Working' technology."
        ],
        "disadvantages": [
            "-10% food production."
        ],
        "start_tech": "bronze_working",
        "bonuses": {
            "food_bonus": -0.1,
        }
    },
    "Chinese": {
        "name": "Chinese",
        "description": "A dynasty known for its scientific achievements and rapid construction.",
        "advantages": ["+50% production towards wonders.", "Start with 'Writing' technology."],
        "disadvantages": ["-10% unit combat strength."],
        "start_tech": "writing",
        "bonuses": { "wonder_production_modifier": 1.5 }
    },
    "English": {
        "name": "English",
        "description": "A maritime empire with a powerful navy and strong economy.",
        "advantages": ["+1 movement for naval units.", "Start with 'Sailing' technology."],
        "disadvantages": ["-10% production for land units."],
        "start_tech": "sailing",
        "bonuses": {}
    },
    "Aztecs": {
        "name": "Aztecs",
        "description": "A fierce, militaristic civilization that grows stronger by capturing enemies.",
        "advantages": ["Gain culture from defeating enemy units.", "Start with 'Agriculture' technology."],
        "disadvantages": ["-20% research speed."],
        "start_tech": "agriculture",
        "bonuses": { "research_bonus": -0.2 }
    },
    "Russians": {
        "name": "Russians",
        "description": "A resilient civilization that thrives in the cold and expands rapidly.",
        "advantages": ["Can found cities in tundra terrain.", "+1 production from tundra tiles."],
        "disadvantages": ["-10% culture generation."],
        "start_tech": "animal_husbandry",
        "bonuses": { "culture_bonus": -0.1 }
    },
}