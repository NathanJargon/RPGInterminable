import pygame
import sys
from dungeonRooms import FirstDungeon
pygame.init()

WIDTH, HEIGHT = 1270, 720
FPS = 60

grid_size = 14
cell_size = min(WIDTH, HEIGHT) // grid_size

rooms = FirstDungeon.rooms1

current_room = 0
grid = rooms[current_room]
player_pos = [0, 0]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

wall_image = pygame.image.load('img/dungeons/walls1.jpg')
floor_image = pygame.image.load('img/dungeons/walls2.jpg')
finish_image = pygame.image.load('img/dungeons/door.png')
player_image = pygame.image.load('img/dungeons/door.png')
wall_image = pygame.transform.scale(pygame.image.load('img/dungeons/walls1.jpg'), (cell_size, cell_size))
floor_image = pygame.transform.scale(pygame.image.load('img/dungeons/walls2.jpg'), (cell_size, cell_size))
finish_image = pygame.transform.scale(pygame.image.load('img/dungeons/door.png'), (cell_size, cell_size))
player_image = pygame.transform.scale(pygame.image.load('img/dungeons/door.png'), (cell_size, cell_size))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and grid[player_pos[1] - 1][player_pos[0]] in [1, 2]:
                player_pos[1] -= 1
            elif event.key == pygame.K_DOWN and grid[player_pos[1] + 1][player_pos[0]] in [1, 2]:
                player_pos[1] += 1
            elif event.key == pygame.K_LEFT and grid[player_pos[1]][player_pos[0] - 1] in [1, 2]:
                player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and grid[player_pos[1]][player_pos[0] + 1] in [1, 2]:
                player_pos[0] += 1
                
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                screen.blit(wall_image, (x * cell_size, y * cell_size))
            elif cell == 1:
                screen.blit(floor_image, (x * cell_size, y * cell_size))
            elif cell == 2:
                screen.blit(finish_image, (x * cell_size, y * cell_size))

    screen.blit(player_image, (player_pos[0] * cell_size, player_pos[1] * cell_size))


    if grid[player_pos[1]][player_pos[0]] == 2:
        current_room += 1
        if current_room < len(rooms):
            grid = rooms[current_room]
            player_pos = [2, 2] 
        else:
            running = False
        
    pygame.display.flip()
    
    pygame.time.Clock().tick(FPS)

pygame.quit()