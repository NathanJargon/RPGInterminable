import random
import time

class MenuAbilityManager:
    def __init__(self):
        self.skills = {
            "Basic Attack": (10, 20, 5, "Deals 10-20 | 5 Stamina Spent"),
            "Langguiser": (20, 30, 10, "Deals 20-30 | 10 Stamina Spent"),
            "Divine Divide": (30, 40, 15, "Deals 30-40 | 15 Stamina Spent"),
            "Soul Steal": (40, 50, 20, "Deals 40-50 | 20 Stamina Spent"),
            "Swift Strike": (15, 25, 10, "Deals 15-25 | 10 Stamina Spent"),
            "Honor's Edge": (25, 35, 15, "Deals 25-35 | 15 Stamina Spent"),
            "Sakura Slash": (35, 45, 20, "Deals 35-45 | 20 Stamina Spent"),
            "Rising Sun Strike": (45, 55, 25, "Deals 45-55 | 25 Stamina Spent"),
            "Zen Blade": (10, 30, 10, "Deals 10-30 | 10 Stamina Spent"),
            "Thundering Katana": (25, 40, 15, "Deals 25-40 | 15 Stamina Spent"),
            "Lotus Fury": (35, 50, 20, "Deals 35-50 | 20 Stamina Spent"),
            "Crescent Moon Cut": (40, 55, 25, "Deals 40-55 | 25 Stamina Spent"),
            "Serenity Sweep": (20, 35, 15, "Deals 20-35 | 15 Stamina Spent"),
            "Tranquil Blade": (30, 45, 20, "Deals 30-45 | 20 Stamina Spent"),
            "Dragon's Breath Slash": (40, 55, 25, "Deals 40-55 | 25 Stamina Spent"),
            "Storm of Petals": (30, 45, 20, "Deals 30-45 | 20 Stamina Spent"),
            "Shogun's Wrath": (35, 50, 25, "Deals 35-50 | 25 Stamina Spent"),
            "Celestial Severance": (45, 60, 30, "Deals 45-60 | 30 Stamina Spent"),
            "Whispering Winds Slice": (25, 40, 20, "Deals 25-40 | 20 Stamina Spent"),
            "Eternal Moonstrike": (50, 70, 35, "Deals 50-70 | 35 Stamina Spent"),
            "Phoenix Dance": (40, 60, 30, "Deals 40-60 | 30 Stamina Spent"),
            "Tsunami Blade": (45, 65, 35, "Deals 45-65 | 35 Stamina Spent"),
            "Silent Storm Slash": (30, 50, 25, "Deals 30-50 | 25 Stamina Spent"),
            "Harmony's Embrace": (35, 55, 30, "Deals 35-55 | 30 Stamina Spent")
        }

        self.items = {
            "Strength Potion": 20,
            "Carnival": 30,
            "Blood Potion": 40,
            "Resurrection": 50,
            "Elixir of Vitality": 25,
            "Guardian's Shield": 35,
            "Mystic Nectar": 45,
            "Phoenix Feather": 55,
            "Lunar Essence": 30,
            "Whirlwind Shuriken": 40,
            "Potion of Serenity": 50,
            "Enchanted Bandage": 60,
            "Soulstone Shard": 35,
            "Ember Ward": 45,
            "Aegis Amulet": 55,
            "Crystal of Renewal": 65,
            "Moonlit Lotus": 40,
            "Pandemonium Elixir": 50,
            "Vampire's Kiss": 60,
            "Golden Revival Charm": 70,
            "Blazing Starlight Infusion": 45,
            "Mystical Draught": 55,
            "Ocean's Tear Gem": 65,
            "Silent Nightshade Extract": 50,
            "Harmony's Blessing": 60
        }

        
        self.run = {
            "Confirm": True,
            "Cancel": True
        }

    def use_skill(self, skill_name, player_stamina):
        if skill_name in self.skills:
            min_damage, max_damage, stamina_cost, description = self.skills[skill_name]
            if player_stamina >= stamina_cost:
                player_stamina -= stamina_cost
                damage = random.randint(min_damage, max_damage)
                return damage, player_stamina
        return 0, player_stamina
    
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
        
    def get_description_by_name(self, name):
        return self.skills[name][3] if name in self.skills else None