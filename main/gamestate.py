from intro import main as intro
from environment import main as environment
from battle import main as battle
from os import path
import pygame
import os
import sys

script_dir = getattr(sys, '_MEIPASS', path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'main'))

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((1270, 720))

    game_state = GameState()

    running = True
    
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            game_state.update()
            try:
                pygame.display.flip()
            except pygame.error:
                pygame.quit()
            pygame.time.Clock().tick(60)
        except pygame.error:
            pygame.quit()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()