import pygame
import pickle
import os
import sys
from os import path
script_dir = getattr(sys, '_MEIPASS', path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'main'))

class Player:
    def __init__(self, x, y, width, height, menu_ability_manager, health=100, stamina=100, attack=10, defense=5, speed=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.level = 2
        self.exp = 0
        self.stamina = stamina
        self.image = pygame.transform.scale(pygame.image.load(self.resource_path('img/player.png')), (width//1.5, height//1.5)) 
        self.show_stats = False
        self.skills = []
        self.items = []
        self.menu_ability_manager = menu_ability_manager
        self.inventory = self.menu_ability_manager.inventory
        self.unlock_skills()
        self.check_equipped_skills()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def save_player(self):
        with open(self.resource_path('savefiles/player_data.pkl'), 'wb') as f:
            pickle.dump((self.exp, self.level), f)

    def load_player(self):
        try:
            with open(self.resource_path('savefiles/player_data.pkl'), 'rb') as f:
                self.exp, self.level = pickle.load(f)
        except EOFError:
            pass
    
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100: 
            self.exp -= self.level * 100
            self.level_up()
        self.save_player()

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
        bar_x = screen.get_width() - bar_width - 450
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
        self.health += 1  
        self.attack += 1
        self.defense += 0.2
        self.speed += 0.2
        self.stamina += 1
        
        self.unlock_skills()
                  
    def check_equipped_skills(self):
        equipped_skills = []
        for skill_name in self.skills:
            if skill_name in self.skills:
                equipped_skills.append(skill_name)
        while len(equipped_skills) < 4:
            equipped_skills.append("None")
        
        return equipped_skills

    def check_equipped_items(self):
        equipped_items = []
        for item_name, (effects, quantity) in self.inventory.items.items():
            if quantity >= 1:
                equipped_items.append(f"{item_name}: {quantity}")
        while len(equipped_items) < 4:
            equipped_items.append("None")
        return equipped_items
    
    def unlock_skills(self):
        skills_to_unlock = {
            1: "Basic Attack",
            2: "Langguiser",
            3: "Divine Divide",
            4: "Soul Steal",
            5: "Swift Strike",
            6: "Honor Edge",
            7: "Sakura Slice",
            8: "Rising Sun",
            9: "Zen Blade",
            10: "Thunder Kat",
        }
        
        for level, skill in skills_to_unlock.items():
            if self.level >= level and skill not in self.skills:
                self.skills.append(skill)
                

    def draw_stats(self, screen, font):
        stats_x = screen.get_width() // 2
        stats_y = (screen.get_height() // 10) - 30

        level_text = font.render(f"Level: {self.level}      Experience: {self.exp}", True, pygame.Color('#FFFFFF'))
        #exp_text = font.render(f"EXP: {self.exp}", True, pygame.Color('#000000')) 

        background_width = level_text.get_width() + 20
        background_height = level_text.get_height() + 20

        #border_width = background_width + 4
        #border_height = background_height + 4 
        #border_x = stats_x - border_width // 2
        #border_y = stats_y - border_height // 2

        #border = pygame.Surface((border_width, border_height))
        #border.fill(pygame.Color('#FFFFFF')) 

        #screen.blit(border, (border_x, border_y))

        # background = pygame.Surface((background_width, background_height))
        # background.set_alpha(128)
        # background.fill(pygame.Color('#FFFFFF'))  

        # screen.blit(background, (stats_x - background.get_width() // 2, stats_y - background.get_height() // 2))

        screen.blit(level_text, (stats_x - level_text.get_width() // 2, stats_y - background_height // 2 + 10))
        #screen.blit(exp_text, (stats_x - exp_text.get_width() // 2, stats_y - background.get_height() // 2 + level_text.get_height() + 10))
        
    
    def draw_menu_button(self, screen, font):
        button_width = 100
        button_height = 50
        button_x = 20
        button_y = screen.get_height() - (button_height + 10)

        border_width = button_width + 4  
        border_height = button_height + 4  
        border_x = button_x - 2  
        border_y = button_y - 2 

        border_rect = pygame.Rect(border_x, border_y, border_width, border_height)
        pygame.draw.rect(screen, ('#00FFFF'), border_rect)

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, ('#223953'), button_rect)

        button_text = font.render('Menu', True, (255, 255, 255))
        screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2, button_y + (button_height - button_text.get_height()) // 2))
        
    
    def handle_menu_button_event(self, event, screen):
        mouse_pos = pygame.mouse.get_pos()
        button_width = 100
        button_height = 50
        button_x = 20
        button_y = screen.get_height() - (button_height + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        if button_rect.collidepoint(mouse_pos):
            self.show_stats = not self.show_stats
            return not self.show_stats