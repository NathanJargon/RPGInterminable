import pygame
import time
import os
import sys
from os import path
script_dir = getattr(sys, '_MEIPASS', path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'main'))

class Menu:
    KEY_PRESS_DELAY = 0.2
    
    def __init__(self, options, descriptions=[]):
        self.options = options
        self.state = 0
        self.option_rects = []
        self.last_key_press_time = 0 
        self.descriptions = descriptions

    def handle_event(self, event):
        current_time = time.time()
        if event.type == pygame.KEYDOWN:
            if current_time - self.last_key_press_time > self.KEY_PRESS_DELAY:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.state = max(0, self.state - 1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.state = min(len(self.options) - 1, self.state + 1)
                self.last_key_press_time = current_time
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.state = i
        # print(f"Current state: {self.state}, Selected skill: {self.options[self.state]}") 
        return self.options[self.state]

    def draw(self, screen, font):
        fill_color = pygame.Color('#223953')
        border_color = pygame.Color('#000000')
        total_width = sum(font.size(option)[0] + 50 for option in self.options[:len(self.options)//2]) - 50 
        if len(self.options) == 3:
            y = screen.get_height() - 70
            x = (screen.get_width() // 2 - total_width // 2) - 135
        elif len(self.options) == 2:
            y = screen.get_height() - 70
            x = (screen.get_width() // 2 - total_width // 2) - 90
        else:
            y = screen.get_height() - 120
            x = (screen.get_width() // 2 - total_width // 2 ) - 20
        self.option_rects = []
        for i, option in enumerate(self.options):
            if i == len(self.options) // 2 and len(self.options) > 3:  
                y += 50  
                x = (screen.get_width() // 2 - total_width // 2) - 50
            color = (0, 255, 255) if i == self.state else (255, 255, 255)
            text = font.render(option, True, color)
            option_rect = pygame.Rect(x-10, y-2, font.size(option)[0] + 40, font.size(option)[1] + 10)
            text_rect = text.get_rect(center=option_rect.center)
            pygame.draw.rect(screen, fill_color, option_rect)
            pygame.draw.rect(screen, border_color, option_rect, 5)
            screen.blit(text, text_rect)
            self.option_rects.append(option_rect)
            x += font.size(option)[0] + 50