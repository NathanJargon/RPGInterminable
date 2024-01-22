import pygame
from menu import Menu
from enemy import Enemy
from player import Player

pygame.init()
pygame.display.set_caption("Interminable")

WIDTH, HEIGHT = 1270, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.display.set_icon(pygame.image.load("img/icon.png"))

clock = pygame.time.Clock()

player_turn = True

font = pygame.font.Font(None, 36)

menu_state = 0
submenu_state = 0

main_menu = Menu(["Skill", "Items", "Run"])
submenus = {
    "Skill": Menu(["Basic Attack", "Langguiser", "Divine Divide", "Soul Steal"]),
    "Items": Menu(["Potion of Strength", "Carnival", "Blood Potion", "Resurrection"]),
    "Run": Menu(["Confirm", "Cancel"])
}

current_menu = main_menu

player = Player(50, 50, 200, 100)
enemy = Enemy(WIDTH - 250, 50, 200, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if player_turn:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    selected_option = current_menu.handle_event(event)
                    if current_menu == main_menu:
                        current_menu = submenus[selected_option]
                    else:
                        print(f"You selected {selected_option}")
                        current_menu = main_menu
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    current_menu.handle_event(event)
                elif event.key == pygame.K_BACKSPACE:
                    if current_menu != main_menu:
                        current_menu = main_menu


    screen.fill((0, 0, 0))
    
    player.draw(screen, font)
    enemy.draw(screen, font)
    
    current_menu.draw(screen, font)
    
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()