import pygame

class Player:
    def __init__(self, x, y, width, height, health=100, stamina=100, attack=10, defense=5, speed=5, level=2, exp=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.level = level
        self.exp = exp
        self.stamina = stamina
        self.image = pygame.transform.scale(pygame.image.load('img/player.png'), (width//1.5, height//1.5)) 
        self.level = level
        self.skills = []
        self.unlock_skills()
        
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100: 
            self.exp -= self.level * 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health += 10  
        self.attack += 2
        self.defense += 1

    def draw_hp_bar(self, screen, font):
        bar_width = 200
        bar_height = 20
        bar_x = 400
        bar_y = screen.get_height() - bar_height - 10 

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * (self.health / 100), bar_height))

        health_text = font.render(f"HP: {self.health}/100", True, (0, 0, 0))
        screen.blit(health_text, (bar_x + (bar_width - health_text.get_width()) / 2, (bar_y + (bar_height - health_text.get_height()) / 2) - 1))

    def draw_stamina_bar(self, screen, font):
        bar_width = 200
        bar_height = 20
        bar_x = screen.get_width() - bar_width - 430
        bar_y = screen.get_height() - bar_height - 10 

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 0, 255), (bar_x, bar_y, bar_width * (self.stamina / 100), bar_height))

        stamina_text = font.render(f"Stamina: {self.stamina}/100", True, (0, 0, 0))
        screen.blit(stamina_text, (bar_x + (bar_width - stamina_text.get_width()) / 2, (bar_y + (bar_height - stamina_text.get_height()) / 2) - 1))
        
    def draw(self, screen, font):
        screen.blit(self.image, self.rect) 
        self.draw_hp_bar(screen, font)
        self.draw_stamina_bar(screen, font)

    def level_up(self):
        self.level += 1
        self.attack += 1
        self.defense += 1
        self.speed += 0.2
        
        self.unlock_skills()
                  
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level_up()

    def check_equipped_skills(self):
        equipped_skills = []
        for skill_name in self.skills:
            if skill_name in self.skills:
                equipped_skills.append(skill_name)
        while len(equipped_skills) < 4:
            equipped_skills.append("None")
        return equipped_skills
    
    def unlock_skills(self):
        skills_to_unlock = {
            1: "Basic Attack",
            2: "Langguiser",
            3: "Divine Divide",
            4: "Soul Steal",
            5: "Swift Strike",
            6: "Honor's Edge",
            7: "Sakura Slash",
            8: "Rising Sun Strike",
            9: "Zen Blade",
            10: "Thundering Katana",
            11: "Lotus Fury",
            12: "Crescent Moon Cut",
            13: "Serenity Sweep",
            14: "Tranquil Blade",
            15: "Dragon's Breath Slash",
            16: "Storm of Petals",
            17: "Shogun's Wrath",
            18: "Celestial Severance",
            19: "Whispering Winds Slice",
            20: "Eternal Moonstrike",
            21: "Phoenix Dance",
            22: "Tsunami Blade",
            23: "Silent Storm Slash",
            24: "Harmony's Embrace"
        }
        
        for level, skill in skills_to_unlock.items():
            if self.level >= level and skill not in self.skills:
                self.skills.append(skill)