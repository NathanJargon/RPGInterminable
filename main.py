import pygame
import random as r

pygame.init()

pygame.display.set_caption("Interminable RPG")
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 36)

#img
main_img = pygame.image.load('img/main.png')
main_img = pygame.transform.scale(main_img, (920-300, 610-300))
enemy_img = pygame.image.load('img/enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (4096-3400, 4096-3400))
bg = pygame.image.load('img/bg.png')
bg = pygame.transform.scale(bg, (2048-750, 2048-1000))

#attack gif
num_frames = 4
attack_x = 450
attack_y = 100 
frame_delay = 100

#global var
in_battle = False

class Character:
    def __init__(self, name, hp, atk, defense):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense

    def attack(self, enemy):
        damage = self.atk - enemy.defense
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        return damage

class Player(Character):
    def __init__(self, name, hp, atk, defense):
        super().__init__(name, hp, atk, defense)
        self.level = 1
        self.exp = 0

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.hp += 10
        self.atk += 2
        self.defense += 1
        self.exp = 0

class Enemy(Character):
    def __init__(self):
        super().__init__("Knight", 50, r.randrange(5), 2)

player = Player("Nash", 100, r.randrange(10), 5)

def draw_text(text, x, y):
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))

def draw_text_fade(text, x, y, fade_time=2000):
    for color in range(0, 256, 5): 
        text_surface = font.render(text, True, (color, color, color))
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        pygame.time.delay(fade_time // 255)

    for color in range(255, -1, -5): 
        text_surface = font.render(text, True, (color, color, color))
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        pygame.time.delay(fade_time // 255)

def draw_choices():
    choices = ["1. Attack", "2. Defend", "3. Run"]
    x = 50
    y = 50
    for choice in choices:
        text_surface = font.render(choice, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        y += 50
        
def handle_battle(event, player, enemy):
    if event.key == pygame.K_1:
        frames = [pygame.image.load(f'img/attack/attack_frame_{i}.png') for i in range(num_frames)]
        scaled_frames = [pygame.transform.scale(frame, (200+500, 159+500)) for frame in frames]


        for frame in scaled_frames:
            screen.blit(frame, (attack_x, attack_y))
            draw_choices()
            pygame.display.flip()
            pygame.time.delay(frame_delay)
            pygame.display.flip()
            pygame.time.delay(frame_delay)

        damage = player.attack(enemy)
        if enemy.hp <= 0:
            player.gain_exp(50)
            return f"{player.name} dealt {damage} damage to {enemy.name}. {enemy.name} has been defeated!", False, True
        return f"{player.name} dealt {damage} damage to {enemy.name}.", True, True
    elif event.key == pygame.K_2:
        return f"{player.name} defends.", True, True 
    elif event.key == pygame.K_3:
        return f"{player.name} runs away.", False, True 
    else:
        return "", in_battle, False
    
def game_loop():
    running = True
    global in_battle
    enemy = None
    message = ""
    fade = False
    fade_done = False 
 
    while running:
        screen.fill((0, 0, 0)) 
        screen.blit(bg, (0, -250))
        screen.blit(enemy_img, (450, 100))
        screen.blit(main_img, (0, 425))
        
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(50, 300, player.hp, 20))
        if enemy:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(700, 70, enemy.hp, 20))

        draw_text(f"{player.name}: {player.hp}/100", 50, 270)
        if enemy:
            draw_text(f"{enemy.name}: {enemy.hp}/100", 700, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and in_battle:
                old_message = message
                message, in_battle, fade = handle_battle(event, player, enemy)
                if old_message != message: 
                    fade_done = False 
                pygame.time.delay(100)


        if player.hp <= 0:
            message = f"{player.name} has been defeated!"
            running = False

        if in_battle:
            draw_text("1. Attack", 50, 50)
            draw_text("2. Defend", 50, 100)
            draw_text("3. Run", 50, 150)

        if fade and not fade_done:
            draw_text_fade(message, 50, 200)
            fade_done = True
        else:
            draw_text(message, 50, 200)
        
        pygame.display.flip()
        
        if not in_battle:
            enemy = Enemy()
            in_battle = True

game_loop()

pygame.quit()