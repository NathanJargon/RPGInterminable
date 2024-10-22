import pygame
from volumeslider import VolumeSlider
from save_and_load import OutsideGameData
import os
import sys

class Pause:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.overlay = pygame.Surface((self.screen_width, self.screen_height)) 
        self.overlay.set_alpha(128)  
        self.overlay.fill((0, 0, 0))
        self.box = pygame.image.load(self.resource_path('img/pause.png')) 
        self.box_rect = self.box.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.slider = VolumeSlider(self.box_rect.x + 50, self.box_rect.y + self.box_rect.height // 2, self.box_rect.width - 100, 20) 

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def draw(self):
        self.screen.blit(self.overlay, (0, 0)) 
        self.screen.blit(self.box, self.box_rect) 
        self.slider.draw(self.screen)

    def handle_event(self, event):
        self.slider.handle_event(event)