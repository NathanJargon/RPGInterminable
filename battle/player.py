import pygame

class Player:
    def __init__(self, x, y, width, height, health=100, attack=10, defense=5, level=1, exp=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.exp = exp
        self.image = pygame.transform.scale(pygame.image.load('img/player.png'), (width//1.5, height//1.5)) 


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
        bar_x = (screen.get_width() - bar_width) / 2
        bar_y = screen.get_height() - bar_height - 10 

        hp_text = font.render("HP", True, (0, 0, 0))
        #screen.blit(hp_text, (bar_x - 40, bar_y - 7))

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * (self.health / 100), bar_height))

        health_text = font.render(f"HP: {self.health}/100", True, (0, 0, 0))
        screen.blit(health_text, (bar_x + (bar_width - health_text.get_width()) / 2, (bar_y + (bar_height - health_text.get_height()) / 2) - 1))
        
    def draw(self, screen, font):
        screen.blit(self.image, self.rect) 
        self.draw_hp_bar(screen, font)