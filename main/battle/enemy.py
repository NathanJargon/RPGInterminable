import pygame
import random
import time

class Enemy:
    def __init__(self, x, y, name, width, height,  min_damage, max_damage, health=100, defense=0, speed=0):
        self.y = y
        self.x = x
        self.name = name
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load('img/enemy.png'), (self.width//1.5, self.height//1.5)) 
        self.font = pygame.font.Font('fonts/Oswald.ttf', 24)
        self.hp_text = pygame.font.Font('fonts/Oswald.ttf', 14)
        self.hover_text = pygame.font.Font('fonts/Oswald.ttf', 12)
        self.health = health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.defense = defense
        self.speed = speed
        self.attacked_already = False
        self.statusbox = pygame.image.load("img/statusbox/knight.png")

    def attacked(self, screen, image):
        self.image = pygame.transform.scale(image, (self.width//1.5, self.height//1.5)) 
        screen.blit(self.image, self.rect)

    def draw(self, screen, paused, image):
        self.attacked(screen, image) 
        enemy_text = self.font.render(self.name, True, (255, 0, 0))
        enemy_text_rect = enemy_text.get_rect(topleft=(self.x + 210, self.y - 70))
        screen.blit(enemy_text, (self.x + 210, self.y - 70))
        hover_text = self.hover_text.render("HOVER to INSPECT Enemy", True, (255, 0, 0))
        screen.blit(hover_text, (self.x + 210, self.y - 80))
        
        hp_bar_width = 100
        hp_bar_height = 10
        pygame.draw.rect(screen, (128, 128, 128), (self.x + 210, self.y - 30, hp_bar_width, hp_bar_height + 5)) 
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 210, self.y - 30, hp_bar_width * (self.health / 100), hp_bar_height + 5))

        hp_text = self.hp_text.render(f"HP: {self.health}", True, (0, 0, 0))
        text_x = self.x + 210 + (hp_bar_width - hp_text.get_width()) // 2  
        text_y = self.y - 28 + (hp_bar_height - hp_text.get_height()) // 2 
        screen.blit(hp_text, (text_x, text_y)) 
        
        self.handle_mouse_over(screen, paused)

    def handle_mouse_over(self, screen, paused):
        if not paused:
            enemy_text_rect = self.font.render(self.name, True, (255, 0, 0)).get_rect(topleft=(self.x + 210, self.y - 70))
            if enemy_text_rect.collidepoint(pygame.mouse.get_pos()):
                enemy_text = self.font.render(self.name, True, (128, 128, 128))
                screen.blit(enemy_text, (self.x + 210, self.y - 70))
                screen.blit(self.statusbox, (50, 10))

              
    def attack(self):
        random.seed(time.time())
        return random.randint(self.min_damage, self.max_damage)