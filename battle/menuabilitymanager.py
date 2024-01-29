import random
import time

class MenuAbilityManager:
    def __init__(self):
        self.skills = {
            "Basic Attack": (10, 20),
            "Langguiser": (20, 30),
            "Divine Divide": (30, 40),
            "Soul Steal": (40, 50)
        }
        self.items = {
            "Strength Potion": 20,
            "Carnival": 30,
            "Blood Potion": 40,
            "Resurrection": 50
        }
        
        self.run = {
            "Confirm": True,
            "Cancel": True
        }

    def use_skill(self, skill_name):
        skill_name = skill_name.strip() 
        if skill_name in self.skills:
            min_damage, max_damage = self.skills[skill_name]
            random.seed(time.time())
            return random.randint(min_damage, max_damage)
        else:
            return None

    def use_item(self, item_name):
        item_name = item_name.strip()
        if item_name in self.items:
            return self.items[item_name]
        else:
            return None

    def use_run(self, run_option):
        run_option = run_option.strip()
        if run_option in self.run:
            return self.run[run_option]
        else:
            return None