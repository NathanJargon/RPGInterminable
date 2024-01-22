import pygame

class Menu:
    def __init__(self, options):
        self.options = options
        self.state = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state = (self.state - 1) % len(self.options)
            elif event.key == pygame.K_RIGHT:
                self.state = (self.state + 1) % len(self.options)
        return self.options[self.state]

    def draw(self, screen, font):
        total_width = sum(font.size(option)[0] + 100 for option in self.options) - 100
        x = screen.get_width() // 2 - total_width // 2
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.state else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (x, screen.get_height() - 60))
            x += font.size(option)[0] + 100