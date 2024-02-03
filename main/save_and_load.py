from inventory import Inventory
from menuabilitymanager import MenuAbilityManager
from volumeslider import VolumeSlider
import pygame
import json

class OutsideGameData:
    def __init__(self, screen, current_room, player_pos, grid, visibility_grid, unlocked, unknown_rendered, text_show):
        # GameData attributes
        self.current_room = current_room
        self.player_pos = player_pos
        self.grid = grid
        self.visibility_grid = visibility_grid
        self.unlocked = unlocked
        self.unknown_rendered = unknown_rendered
        self.text_show = text_show
        self.menu_ability_manager = MenuAbilityManager()
        
        # DataButton attributes
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.overlay = pygame.Surface((self.screen_width, self.screen_height)) 
        self.overlay.set_alpha(128)  
        self.overlay.fill((0, 0, 0))
        self.box = pygame.image.load('img/pause.png') 
        self.box_rect = self.box.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.slider = VolumeSlider(self.box_rect.x + 50, self.box_rect.y + self.box_rect.height // 2, self.box_rect.width - 100, 20) 
        self.save_button_color = pygame.Color('#FFFFFF')
        self.load_button_color = pygame.Color('#FFFFFF')
        
        # Create save and load buttons
        self.button_height = 50
        self.font = pygame.font.Font("fonts/Oswald.ttf", 24)
        self.save_button = pygame.Rect(self.slider.rect.x, self.slider.rect.bottom + 10, self.slider.rect.width, self.button_height)
        self.load_button = pygame.Rect(self.slider.rect.x, self.save_button.bottom + 10, self.slider.rect.width, self.button_height)

    def reset_game(self, game_data=None):
        if game_data is None:
            self.current_room = None
            self.player_pos = None
            self.grid = None
            self.visibility_grid = None
            self.unlocked = None
            self.unknown_rendered = None
            self.text_show = None
        else:
            self.current_room = game_data['current_room']
            self.player_pos = game_data['player_pos']
            self.grid = game_data['grid']
            self.visibility_grid = game_data['visibility_grid']
            self.unlocked = game_data['unlocked']
            self.unknown_rendered = game_data['unknown_rendered']
            self.text_show = game_data['text_show']

    def save_game(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.current_room_save(), f)

    @staticmethod
    def load_game(filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def current_room_save(self):
        return {
            'current_room': self.current_room,
            'player_pos': self.player_pos,
            'grid': self.grid,
            'visibility_grid': self.visibility_grid,
            'unlocked': self.unlocked,
            'unknown_rendered': self.unknown_rendered,
            'text_show': self.text_show
        }

    def draw(self):
        fill_color = pygame.Color('#223953')
        border_color = pygame.Color('#000000')
        self.screen.blit(self.overlay, (0, 0)) 
        self.screen.blit(self.box, self.box_rect) 
        self.slider.draw(self.screen)

        pygame.draw.rect(self.screen, border_color, self.save_button, 2) 
        pygame.draw.rect(self.screen, fill_color, self.save_button.inflate(-4, -4)) 
        pygame.draw.rect(self.screen, border_color, self.load_button, 2)  
        pygame.draw.rect(self.screen, fill_color, self.load_button.inflate(-4, -4))  

        pygame.draw.rect(self.screen, self.save_button_color, self.save_button.inflate(-4, -4)) 
        pygame.draw.rect(self.screen, self.load_button_color, self.load_button.inflate(-4, -4))  

        save_text = self.font.render('Save', True, (0, 0, 0))
        load_text = self.font.render('Load', True, (0, 0, 0))
        self.screen.blit(save_text, (self.save_button.x + (self.save_button.width - save_text.get_width()) // 2, self.save_button.y + (self.save_button.height - save_text.get_height()) // 2))
        self.screen.blit(load_text, (self.load_button.x + (self.load_button.width - load_text.get_width()) // 2, self.load_button.y + (self.load_button.height - load_text.get_height()) // 2))
        
    def handle_event(self, event):
        self.slider.handle_event(event)
        unpause = False
        loaded_data = None

        if event.type == pygame.MOUSEMOTION:
            if self.save_button.collidepoint(event.pos):
                self.save_button_color = pygame.Color('#223953') 
            else:
                self.save_button_color = pygame.Color('#FFFFFF') 
                
            if self.load_button.collidepoint(event.pos):
                self.load_button_color = pygame.Color('#223953') 
            else:
                self.load_button_color = pygame.Color('#FFFFFF') 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.collidepoint(event.pos):
                self.save_game('savefiles/save_file.json')
                unpause = True
            elif self.load_button.collidepoint(event.pos):
                loaded_data = self.load_game('savefiles/save_file.json')
                unpause = True

        return unpause, loaded_data
