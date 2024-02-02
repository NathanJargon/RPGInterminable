import pygame
import random
import math
import time
from menu import Menu
from enemy import Enemy
from player import Player
from menuabilitymanager import MenuAbilityManager
from pause import Pause
from inventory import Inventory
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Interminable - Battle")

def main():
    WIDTH, HEIGHT = 1270, 720
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    icon = pygame.display.set_icon(pygame.image.load("img/icon.png"))
    menu_rect = pygame.image.load("img/menubox.png")
    menu_ability = pygame.image.load("img/menuboxability.png")
    bg = pygame.image.load("img/bg.jpg")
    clock = pygame.time.Clock()

    player_turn = True
    damage = None
    enemyDamageText = None
    hp_gain = None      
    running = True
    paused = False
    menu_current = menu_rect

    enemy_w, enemy_h = 800, 650

    enemy_attack_sound = pygame.mixer.Sound('ost/sounds/enemy.mp3')
    enemy_attack_sound.set_volume(50)
    
    player_attack_sound = pygame.mixer.Sound('ost/sounds/player.mp3')
    player_attack_sound.set_volume(50)
    
    attack_image = pygame.image.load('img/attacked.png')
    attack_image = pygame.transform.scale(attack_image, (WIDTH, HEIGHT))
    
    enemy_image = pygame.image.load('img/enemy.png')
    enemy_attacked = pygame.image.load("img/enemyattacked.png")
    
    font = pygame.font.Font(None, 36)
    hp_text = pygame.font.Font("fonts/Oswald.ttf", 20)
    game_text = pygame.font.Font('fonts/Oswald.ttf', 24)

    fill_color = pygame.Color('#223953')
    border_color = pygame.Color('#000000')
    pygame.mixer.music.load("ost/fight1.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(25)
    
    pause = Pause(screen)
    inventory = Inventory()
    menu_ability_manager = MenuAbilityManager()
    player = Player(0, 390, 1000, 500, menu_ability_manager)
    enemy = Enemy(WIDTH - 650, 200, "—Knight—",  enemy_w, enemy_h, 10, 20)
    skills = MenuAbilityManager()
    player_attack_calculated = player.attack // 5
    equipped_skills = player.check_equipped_skills()
    equipped_items = player.check_equipped_items()
    equipped_skill_descriptions = [skills.get_description_by_name(name) for name in equipped_skills]

    menu_state = 0
    submenu_state = 0

    main_menu = Menu(["Skill", "Items", "Run"], equipped_skill_descriptions)
    submenus = {
        "Skill": Menu(equipped_skills),
        "Items": Menu(equipped_items),
        "Run": Menu(["Confirm", "Cancel"])
    }

    current_menu = main_menu


    def enemyAttack():
        pygame.time.delay(1000)
        enemy_damage = enemy.attack()
        reduced_damage = calculate_damage_after_defense(enemy_damage, player.defense)
        # print("Enemy:", reduced_damage)
        enemyDamageText = player.health - reduced_damage
        player.health = max(enemyDamageText, 0)
        return reduced_damage

    def calculate_damage_after_defense(damage, defense):
        reduced_damage = (damage + player_attack_calculated) - defense
        reduced_damage = max(reduced_damage, 0)
        random.seed(time.time())
        reduced_damage = reduced_damage * random.uniform(0.85, 1.15)
        return math.floor(reduced_damage)

    while running:
        
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))
        enemy.draw(screen, font, enemy_image)
            
        if not player_turn:
            enemyDamageText = enemyAttack()
            player_turn = True
            enemy_attack_sound.play()
            
            pygame.time.wait(500)
                        
            screen.blit(attack_image, (0, 0)) 
            pygame.display.flip()

            pygame.time.wait(1000)

        if player_turn and current_menu == submenus["Skill"] and not paused and not enemy.attacked_already:
            menu_ability_manager = MenuAbilityManager()
            skill_name = current_menu.options[current_menu.state]
            if skill_name != "None":
                description = menu_ability_manager.skills[skill_name][3]
                text = game_text.render(description, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 180))
                description_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 2, text_rect.width + 20, text_rect.height + 5)
                pygame.draw.rect(screen, fill_color, description_rect)
                pygame.draw.rect(screen, border_color, description_rect, 5)
                screen.blit(text, text_rect)

        if player_turn and current_menu == submenus["Items"] and not paused and not enemy.attacked_already:
            menu_ability_manager = MenuAbilityManager()
            item_name = (current_menu.options[current_menu.state]).split(":")[0]
            if item_name != "None":
                description = menu_ability_manager.items[item_name][0][2]
                text = game_text.render(description, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 180))
                description_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 2, text_rect.width + 20, text_rect.height + 5)
                pygame.draw.rect(screen, fill_color, description_rect)
                pygame.draw.rect(screen, border_color, description_rect, 5)
                screen.blit(text, text_rect)
            
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
                                if skill_name != "None":
                                    damage, player.stamina = skills.use_skill(skill_name, player.stamina) 
                                    if damage is not None:
                                        reduced_damage = calculate_damage_after_defense(damage, enemy.defense)
                                        enemy.health = max(enemy.health - reduced_damage, 0)
                                        player_turn = False
                                        player_attack_sound.play()
                                        pygame.time.wait(500)
        
                                        enemy.image = enemy_attacked  
                                        screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))
                                        enemy.draw(screen, font, enemy_attacked)
                                        pygame.display.flip()
                                        
                                        pygame.time.wait(1000) 

                                        enemy.image = enemy_image 
                                        pygame.display.flip()
                                        
                                        menu_current = menu_rect
                                        current_menu = main_menu
                                        
                            elif main_menu.state == 1:
                                item_name = selected_option
                                item_count = (current_menu.options[current_menu.state]).split(":")[1]
                                if item_name != "None" and int(item_count) > 0:
                                    hp_gain, mp_gain, new_count = skills.use_item(item_name)
                                    if hp_gain is not None:
                                        player.health = min(player.health + hp_gain, 100)
                                    if mp_gain is not None:
                                        player.stamina = min(player.stamina + mp_gain, 100)
                                    player_turn = False
                                    menu_current = menu_rect
                                    current_menu = main_menu

                                    item_name = item_name.split(":")[0].strip()
                                    submenus["Items"].options[submenus["Items"].state] = f"{item_name}: {new_count}"
                                    
                                    
                            elif main_menu.state == 2:
                                if selected_option == "Confirm":
                                    running = False
                                else:
                                    current_menu = main_menu
                                    menu_current = menu_rect
                    elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
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
                            if selected_option == 'Run': 
                                menu_current = menu_rect 
                            else:
                                menu_current = menu_ability
                            current_menu = submenus[selected_option]
                        else:
                            if main_menu.state == 0: 
                                skill_name = selected_option
                                if skill_name != "None":
                                    damage, player.stamina = skills.use_skill(skill_name, player.stamina) 
                                    if damage is not None:
                                        reduced_damage = calculate_damage_after_defense(damage, enemy.defense)
                                        enemy.health = max(enemy.health - reduced_damage, 0)
                                        player_turn = False
                                        player_attack_sound.play()
                                        
                                        pygame.time.wait(500)
        
                                        enemy.image = enemy_attacked  
                                        screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))
                                        enemy.attacked(screen, enemy_attacked)
                                        pygame.display.flip()
                                        
                                        pygame.time.wait(1000) 

                                        enemy.image = enemy_image 
                                        pygame.display.flip()
                                        
                                        menu_current = menu_rect
                                        current_menu = main_menu
                                        
                                        
                            elif main_menu.state == 1:
                                item_name = selected_option
                                item_count = (current_menu.options[current_menu.state]).split(":")[1]
                                if item_name != "None" and int(item_count) > 0:
                                    hp_gain, mp_gain, new_count = skills.use_item(item_name)
                                    if hp_gain is not None:
                                        player.health = min(player.health + hp_gain, 100)
                                    if mp_gain is not None:
                                        player.stamina = min(player.stamina + mp_gain, 100)
                                    player_turn = False
                                    menu_current = menu_rect
                                    current_menu = main_menu

                                    item_name = item_name.split(":")[0].strip()
                                    submenus["Items"].options[submenus["Items"].state] = f"{item_name}: {new_count}"
                                    
                                    
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
                    text = game_text.render(f"You selected {selected_option.split(':')[0]} and healed {hp_gain} HP and {mp_gain} MP", True, (0, 0, 0))
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
    

if __name__ == "__main__":
    main()