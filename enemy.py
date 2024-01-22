import pygame

class Enemy:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, font):
        pygame.draw.rect(screen, (255, 0, 255), self.rect, 2)
        enemy_text = font.render("Enemy", True, (255, 255, 255))
        screen.blit(enemy_text, (self.rect.x + (self.rect.width - enemy_text.get_width()) // 2, self.rect.y + (self.rect.height - enemy_text.get_height()) // 2))