from intro import main as intro
from environment import main as environment
from battle import main as battle
import pygame

class GameState:
    def __init__(self):
        self.state = "START"

    def start(self):
        next_state = intro()
        if next_state == 'ENVIRONMENT':
            self.state = 'ENVIRONMENT'

    def environment(self):
        next_state = environment()
        if next_state == 'BATTLE':
            self.state = 'BATTLE'

    def battle(self):
        next_state = battle()
        if next_state == 'ENVIRONMENT':
            self.state = 'ENVIRONMENT'

    def update(self):
        if self.state == "START":
            self.start()
        elif self.state == "ENVIRONMENT":
            self.environment()
        elif self.state == "BATTLE":
            self.battle()

pygame.init()
screen = pygame.display.set_mode((1270, 720))

game_state = GameState()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_state.update()

    pygame.display.flip() 

pygame.quit()