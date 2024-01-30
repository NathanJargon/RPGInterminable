import pygame
import time

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
                if event.key == pygame.K_LEFT:
                    self.state = max(0, self.state - 1)
                elif event.key == pygame.K_RIGHT:
                    self.state = min(len(self.options) - 1, self.state + 1)
                self.last_key_press_time = current_time
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.state = i
        # print(f"Current state: {self.state}, Selected skill: {self.options[self.state]}") 
        return self.options[self.state]

    def draw_description(self, screen, font):
        description = self.descriptions[self.state] if self.state < len(self.descriptions) else None
        if description:
            description_text = font.render(description, True, (255, 255, 255))
            description_rect = description_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
            screen.blit(description_text, description_rect)
        
    def draw(self, screen, font):
        fill_color = pygame.Color('#223953')
        border_color = pygame.Color('#000000')
        total_width = sum(font.size(option)[0] + 50 for option in self.options[:len(self.options)//2]) - 50 
        if len(self.options) == 3:
            y = screen.get_height() - 70
            x = (screen.get_width() // 2 - total_width // 2) - 100
        elif len(self.options) == 2:
            y = screen.get_height() - 70
            x = (screen.get_width() // 2 - total_width // 2) - 65
        else:
            y = screen.get_height() - 120
            x = screen.get_width() // 2 - total_width // 2 
        self.option_rects = []
        for i, option in enumerate(self.options):
            if i == len(self.options) // 2 and len(self.options) > 3:  
                y += 50  
                x = screen.get_width() // 2 - total_width // 2 
            color = (0, 255, 255) if i == self.state else (255, 255, 255)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(x + font.size(option)[0] // 2, y + font.size(option)[1] // 2))
            option_rect = pygame.Rect(x-10, y-2, font.size(option)[0] + 20, font.size(option)[1] + 5)
            pygame.draw.rect(screen, fill_color, option_rect)
            pygame.draw.rect(screen, border_color, option_rect, 5)
            screen.blit(text, text_rect)
            self.option_rects.append(option_rect)
            x += font.size(option)[0] + 50 