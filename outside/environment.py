import pygame
import sys
from dungeonRooms import FirstDungeon
pygame.init()
pygame.display.set_caption("Interminable - Dungeon")

WIDTH, HEIGHT = 1270, 720
FPS = 60

grid_size = 14
cell_size = min(WIDTH, HEIGHT) // grid_size


current_room = 0
dungeon_length = FirstDungeon.rooms1
rooms_grid = FirstDungeon.rooms1[current_room][0]
description = FirstDungeon.rooms1[current_room][1]
grid = rooms_grid
player_pos = [0, 0]
visibility_radius = 1
unlocked = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))


wall_image = pygame.transform.scale(pygame.image.load('img/dungeons/wall.jpg'), (cell_size, cell_size))
floor_image = pygame.transform.scale(pygame.image.load('img/dungeons/walls1.jpg'), (cell_size, cell_size))
door_image = pygame.transform.scale(pygame.image.load('img/dungeons/door.png'), (cell_size, cell_size))
lever_image = pygame.transform.scale(pygame.image.load('img/dungeons/lever.png'), (cell_size, cell_size))
lever_done_image = pygame.transform.scale(pygame.image.load('img/dungeons/leverdone.png'), (cell_size, cell_size))
locked_image = pygame.transform.scale(pygame.image.load('img/dungeons/locked.png'), (cell_size, cell_size))
player_left = pygame.transform.scale(pygame.image.load('img/movement/left.png'), (cell_size, cell_size))
player_right = pygame.transform.scale(pygame.image.load('img/movement/right.png'), (cell_size, cell_size))
player_idle = pygame.transform.scale(pygame.image.load('img/movement/right.png'), (cell_size, cell_size))

unknown_image = pygame.image.load('img/dungeons/walls1.jpg').convert_alpha()
unknown_image.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

unknown_rendered = False

text_font = pygame.font.Font('fonts/Oswald.ttf', 24)
room_text = text_font.render(description, True, (255, 255, 255))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (grid[player_pos[1] - 1][player_pos[0]] in [1, 2, 3] or (grid[player_pos[1] - 1][player_pos[0]] in [4] and unlocked)):
                player_pos[1] -= 1
                player_idle = player_right
            elif event.key == pygame.K_DOWN and (grid[player_pos[1] + 1][player_pos[0]] in [1, 2, 3] or (grid[player_pos[1] - 1][player_pos[0]] in [4] and unlocked)):
                player_pos[1] += 1
                player_idle = player_right
            elif event.key == pygame.K_LEFT and (grid[player_pos[1]][player_pos[0] - 1] in [1, 2, 3] or (grid[player_pos[1] - 1][player_pos[0]] in [4] and unlocked)):
                player_pos[0] -= 1
                player_idle = player_left
            elif event.key == pygame.K_RIGHT and (grid[player_pos[1]][player_pos[0] + 1] in [1, 2, 3] or (grid[player_pos[1] - 1][player_pos[0]] in [4] and unlocked)):
                player_pos[0] += 1
                player_idle = player_right

    if not unknown_rendered: # remove if statement to enable fog of war
        for y, row in enumerate(grid): # comment all of this if fog of war needs to be disabled!
            for x, cell in enumerate(row):
                screen.blit(pygame.transform.scale(unknown_image, (cell_size, cell_size)), (x * cell_size, y * cell_size))
            unknown_rendered = True
    
            
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if abs(x - player_pos[0]) <= visibility_radius and abs(y - player_pos[1]) <= visibility_radius:
                if cell == 0:
                    image_alpha = wall_image.copy()
                    image_alpha.set_alpha(255)
                    screen.blit(image_alpha, (x * cell_size, y * cell_size))
                elif cell == 1:
                    image_alpha = floor_image.copy()
                    image_alpha.set_alpha(255)
                    screen.blit(image_alpha, (x * cell_size, y * cell_size))
                elif cell == 2:
                    screen.blit(door_image, (x * cell_size, y * cell_size))
                elif cell == 3:
                    screen.blit(lever_image, (x * cell_size, y * cell_size))
                elif cell == 4:
                    screen.blit(locked_image, (x * cell_size, y * cell_size))

    screen.blit(player_idle, (player_pos[0] * cell_size, player_pos[1] * cell_size))
    screen.blit(room_text, (5,0))

    if not unlocked:
        if grid[player_pos[1]][player_pos[0]] == 3:
            locked_image = door_image
            unlocked = True

    if grid[player_pos[1]][player_pos[0]] == 2 or (grid[player_pos[1]][player_pos[0]] == 4 and unlocked):
        current_room += 1
        if current_room < len(dungeon_length):
            screen.fill('black')
            locked_image = locked_image
            unlocked = False
            unknown_rendered = False
            rooms_grid = FirstDungeon.rooms1[current_room]
            description = FirstDungeon.rooms1[current_room][1]
            grid = rooms_grid[0]
            room_text = text_font.render(description, True, (255, 255, 255))
            player_pos = [0, 0] 
        else:
            running = False
        
    pygame.display.flip()
    
    pygame.time.Clock().tick(FPS)

pygame.quit()