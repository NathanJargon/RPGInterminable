import pygame

class Player:
    def __init__(self, x, y, width, height, health=100, attack=10, defense=5, level=1, exp=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.exp = exp

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:  # Level up every 100 exp
            self.exp -= self.level * 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health += 10  # Increase stats when leveling up
        self.attack += 2
        self.defense += 1

    def draw_hp_bar(self, screen, font):
        # Calculate the position of the HP bar
        bar_width = 200
        bar_height = 20
        bar_x = (screen.get_width() / 2 - bar_width / 2) + 25
        bar_y = screen.get_height() - bar_height - 10  # 10 pixels from the bottom

        # Draw the HP text
        hp_text = font.render("HP", True, (255, 255, 255))
        screen.blit(hp_text, (bar_x - 40, bar_y - 2))

        # Draw the HP bar background (grey bar)
        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        # Draw the HP bar (green bar)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * (self.health / 100), bar_height))

        # Draw the player's health centered in the HP bar
        health_text = font.render(f"{self.health}/100", True, (255, 255, 255))
        screen.blit(health_text, (bar_x + (bar_width - health_text.get_width()) / 2, bar_y + (bar_height - health_text.get_height()) / 2))

    def draw(self, screen, font):
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)
        player_text = font.render("Player", True, (255, 255, 255))
        screen.blit(player_text, (self.rect.x + (self.rect.width - player_text.get_width()) // 2, self.rect.y + (self.rect.height - player_text.get_height()) // 2))

        # Draw the HP bar
        self.draw_hp_bar(screen, font)