import random

class MenuAbilityManager:
    def __init__(self):
        self.skills = {
            "Basic Attack": (10, 20),
            "Langguiser": (20, 30),
            "Divine Divide": (30, 40),
            "Soul Steal": (40, 50)
        }
        self.items = {
            "Potion of Strength": 20,
            "Carnival": 30,
            "Blood Potion": 40,
            "Resurrection": 50
        }

    def use_skill(self, skill_name):
        if skill_name in self.skills:
            min_damage, max_damage = self.skills[skill_name]
            return random.randint(min_damage, max_damage)
        else:
            return None

    def use_item(self, item_name):
        if item_name in self.items:
            return self.items[item_name]
        else:
            return None