BELIEFS = {
    "pantheon": {
        "divine_spark": {
            "name": "Divine Spark",
            "description": "+1 Great Person point from Holy Sites.",
            "effect": {"type": "great_person_points", "amount": 1}
        },
        "sacred_path": {
            "name": "Sacred Path",
            "description": "+1 Culture from Rainforest tiles.",
            "effect": {"type": "yield", "tile": "rainforest", "yield": "culture", "amount": 1}
        }
    },
    "follower": {
        "divine_inspiration": {
            "name": "Divine Inspiration",
            "description": "All World Wonders provide +4 Faith.",
            "effect": {"type": "wonder_yield", "yield": "faith", "amount": 4}
        }
    }
}

class Religion:
    def __init__(self, name, founder_civ):
        self.name = name
        self.founder = founder_civ
        self.beliefs = []
        self.holy_city = None

    def add_belief(self, belief_type, belief_key):
        if belief_type in BELIEFS and belief_key in BELIEFS[belief_type]:
            self.beliefs.append(BELIEFS[belief_type][belief_key])