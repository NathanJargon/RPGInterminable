import random
import time
from inventory import Inventory

class MenuAbilityManager:
    def __init__(self):
        
        self.skills = {
            "Basic Attack": (10, 20, 5, "Deals 10-20 | 5 Stamina Spent"),
            "Langguiser": (20, 30, 10, "Deals 20-30 | 10 Stamina Spent"),
            "Divine Divide": (30, 40, 15, "Deals 30-40 | 15 Stamina Spent"),
            "Soul Steal": (40, 50, 20, "Deals 40-50 | 20 Stamina Spent"),
            "Swift Strike": (15, 25, 10, "Deals 15-25 | 10 Stamina Spent"),
            "Honor Edge": (25, 35, 15, "Deals 25-35 | 15 Stamina Spent"),
            "Sakura Slice": (35, 45, 20, "Deals 35-45 | 20 Stamina Spent"),
            "Rising Sun": (45, 55, 25, "Deals 45-55 | 25 Stamina Spent"),
            "Zen Blade": (10, 30, 10, "Deals 10-30 | 10 Stamina Spent"),
            "Thunder Kat": (25, 40, 15, "Deals 25-40 | 15 Stamina Spent"),
        }

        self.items = {
            "HP Potion": ((20, 0, "Restores 20 HP"), 0),
            "Stamina Potion": ((0, 20, "Restores 20 MP"), 0),
            "Mixed Potion": ((10, 10, "Restores 10 HP and 10 MP"), 0),
            "Revival Potion": ((30, 30, "Restores 30 HP and 30 MP"), 0)
        }
        
        self.run = {
            "Confirm": True,
            "Cancel": True
        }

        self.inventory = Inventory()
        self.inventory.add_debug_items()
        
    def use_skill(self, skill_name, player_stamina):
        if skill_name in self.skills:
            min_damage, max_damage, stamina_cost, description = self.skills[skill_name]
            if player_stamina >= stamina_cost:
                player_stamina -= stamina_cost
                damage = random.randint(min_damage, max_damage)
                return damage, player_stamina
        return 0, player_stamina
    
    def use_item(self, item_name):
        item_name = item_name.strip().split(":")[0]
        if item_name in self.inventory.items:
            effects, count = self.inventory.items[item_name]
            if count > 0:
                hp_restored, mp_restored, description = effects
                new_count = count - 1
                self.inventory.update_item(item_name, (effects, new_count))
                return hp_restored, mp_restored, new_count
        return 0, 0, 0

    def use_run(self, run_option):
        run_option = run_option.strip()
        if run_option in self.run:
            return self.run[run_option]
        else:
            return None
        
    def get_description_by_name(self, name):
        return self.skills[name][3] if name in self.skills else None