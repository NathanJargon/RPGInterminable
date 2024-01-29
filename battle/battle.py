import pygame
import random
import math
import time
from menu import Menu
from enemy import Enemy
from player import Player
from menuabilitymanager import MenuAbilityManager
from pause import Pause
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Interminable")

WIDTH, HEIGHT = 1270, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.display.set_icon(pygame.image.load("img/icon.png"))
menu_rect = pygame.image.load("img/menubox.png")
menu_ability = pygame.image.load("img/menuboxability.png")
bg = pygame.image.load("img/bg.png")
clock = pygame.time.Clock()

player_turn = True
damage = None
enemyDamageText = None
hp_gain = None      
running = True
paused = False
menu_current = menu_rect
pause = Pause(screen)

font = pygame.font.Font(None, 36)
hp_text = pygame.font.Font("fonts/Oswald.ttf", 20)
game_text = pygame.font.Font('fonts/Oswald.ttf', 24)


pygame.mixer.music.load("ost/fight1.mp3")
pygame.mixer.music.play(-1)
 
 
menu_state = 0
submenu_state = 0

main_menu = Menu(["Skill", "Items", "Run"])
submenus = {
    "Skill": Menu(["Basic Attack    ", "Langguiser", "Divine Divide  ", "Soul Steal"]),
    "Items": Menu(["Strength Potion", "Carnival", "Blood Potion     ", "Resurrection"]),
    "Run": Menu(["Confirm", "Cancel"])
}

current_menu = main_menu

player = Player(0, 390, 1000, 500)
enemy = Enemy(WIDTH - 650, 200, "—Knight—",  800, 650, 10, 20)
skills = MenuAbilityManager()

def enemyAttack():
    pygame.time.delay(1000)
    enemy_damage = enemy.attack()
    reduced_damage = calculate_damage_after_defense(enemy_damage, player.defense)
    # print("Enemy:", reduced_damage)
    enemyDamageText = player.health - reduced_damage
    player.health = max(enemyDamageText, 0)
    return reduced_damage

def calculate_damage_after_defense(damage, defense):
    reduced_damage = damage - defense
    reduced_damage = max(reduced_damage, 0)
    random.seed(time.time())
    reduced_damage = reduced_damage * random.uniform(0.85, 1.15)
    return math.floor(reduced_damage)

while running:
    
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))

    if not player_turn:
        enemyDamageText = enemyAttack()
        player_turn = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pause.draw()
                    pygame.display.flip()
                continue
            elif player_turn:
                selected_option = current_menu.handle_event(event)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if current_menu == main_menu:
                        if selected_option in ["Skill", "Items"]:
                            menu_current = menu_ability
                        else:
                            menu_current = menu_rect
                        current_menu = submenus[selected_option]
                    else:
                        if main_menu.state == 0: 
                            skill_name = selected_option
                            damage = skills.use_skill(skill_name)
                            if damage is not None:
                                reduced_damage = calculate_damage_after_defense(damage, enemy.defense)
                                # print("Player:", reduced_damage)
                                enemy.health = max(enemy.health - reduced_damage, 0)
                                player_turn = False
                                menu_current = menu_rect
                                current_menu = main_menu
                        elif main_menu.state == 1:
                            item_name = selected_option
                            hp_gain = skills.use_item(item_name)
                            if hp_gain is not None:
                                player.health = min(player.health + hp_gain, 100)
                                player_turn = False
                                menu_current = menu_rect
                                current_menu = main_menu
                        elif main_menu.state == 2:
                            if selected_option == "Confirm":
                                running = False
                            else:
                                current_menu = main_menu
                                menu_current = menu_rect
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    current_menu.handle_event(event)
                elif event.key == pygame.K_BACKSPACE:
                    if current_menu != main_menu:
                        current_menu = main_menu
                        menu_current = menu_rect
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if current_menu != main_menu:
                        current_menu = main_menu
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_turn:
                selected_option = current_menu.handle_event(event)
                if event.button == 1 and not paused:
                    if current_menu == main_menu:
                        menu_current = menu_ability
                        current_menu = submenus[selected_option]
                    else:
                        if main_menu.state == 0: 
                            skill_name = selected_option
                            damage = skills.use_skill(skill_name)
                            if damage is not None:
                                reduced_damage = calculate_damage_after_defense(damage, enemy.defense)
                                enemy.health = max(enemy.health - reduced_damage, 0)
                                player_turn = False
                                menu_current = menu_rect
                        elif main_menu.state == 1:
                            item_name = selected_option
                            hp_gain = skills.use_item(item_name)
                            if hp_gain is not None:
                                player.health = min(player.health + hp_gain, 100)
                                player_turn = False
                                menu_current = menu_rect
                        elif main_menu.state == 2:
                            if selected_option == "Confirm":
                                running = False
                            else:
                                current_menu = main_menu
                                menu_current = menu_rect
                        current_menu = main_menu
                elif event.button == 3:
                    if current_menu != main_menu:
                        current_menu = main_menu
        elif event.type == pygame.MOUSEMOTION:
            if player_turn:
                current_menu.handle_event(event)
        if paused:
            pause.slider.handle_event(event)
            pause.draw()
            pygame.display.flip()
        else:
            enemy.handle_mouse_over(screen, paused)
            
    if paused:
        continue      
    
    if not paused:
        enemy.handle_mouse_over(screen, paused) 
        
    enemy.draw(screen, font)
    screen.blit(menu_current, (0, HEIGHT-150))
    player.draw(screen, hp_text)
    current_menu.draw(screen, font)
    
    if not player_turn and current_menu == main_menu:
        if main_menu.state == 0: 
            if damage is not None:
                text = game_text.render(f"You selected {selected_option.strip()} and dealt {damage} damage", True, (0, 0, 0))
                text_rect = text.get_rect(center=((WIDTH // 2) + 20, (HEIGHT // 2) + 240))
                screen.blit(text, text_rect) 
        elif main_menu.state == 1:
            if hp_gain is not None:
                text = game_text.render(f"You selected {selected_option.strip()} and healed {hp_gain} HP", True, (0, 0, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 240))
                screen.blit(text, text_rect) 

    if player_turn and current_menu == main_menu:
        if damage is not None:
            menu_current = menu_rect
            text = game_text.render(f"{enemy.name} attacked and dealt {enemyDamageText} damage", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 240))
            screen.blit(text, text_rect) 
    
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()