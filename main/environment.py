import pygame
import sys
from dungeonRooms import FirstDungeon
from dialogues import Dialogues
from save_and_load import OutsideGameData
import random

pygame.init()
pygame.display.set_caption("Interminable")

def main():
    WIDTH, HEIGHT = 1270, 720
    FPS = 60

    grid_size = 14
    cell_size = min(WIDTH, HEIGHT) // grid_size

    current_room = 0
    dungeon_length = FirstDungeon.rooms1
    rooms_grid = FirstDungeon.rooms1[current_room][0]
    description = FirstDungeon.rooms1[current_room][1]
    grid = rooms_grid
    player_pos = FirstDungeon.rooms1[current_room][2]
    current_dialogue = Dialogues.dialogue1[current_room]
    visibility_radius = 1
    visibility_grid = [[False for _ in row] for row in grid]
    unlocked = False

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    paused = False

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
    text_show = False

    text_font = pygame.font.Font('fonts/Oswald.ttf', 24)
    room_text = text_font.render(description, True, (255, 255, 255))

    pause = OutsideGameData(screen, current_room, player_pos, grid, visibility_grid, unlocked, unknown_rendered, text_show)

    def battleProbability():
        return random.randint(1, 10)
    
    def fade():
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))

        for alpha in range(0, 300, 2):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)
            
            
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and (grid[player_pos[1] - 1][player_pos[0]] in [1, 2, 3] or (grid[player_pos[1] - 1][player_pos[0]] == 4 and unlocked)):
                    player_pos[1] -= 1
                    player_idle = player_right
                    if battleProbability() == 1:
                        fade()
                        return 'BATTLE'
                elif event.key == pygame.K_DOWN and (grid[player_pos[1] + 1][player_pos[0]] in [1, 2, 3] or (grid[player_pos[1] + 1][player_pos[0]] == 4 and unlocked)):
                    player_pos[1] += 1
                    player_idle = player_right
                    if battleProbability() == 1:
                        fade()
                        return 'BATTLE'
                elif event.key == pygame.K_LEFT and (grid[player_pos[1]][player_pos[0] - 1] in [1, 2, 3] or (grid[player_pos[1]][player_pos[0] - 1] == 4 and unlocked)):
                    player_pos[0] -= 1
                    player_idle = player_left
                    if battleProbability() == 1:
                        fade()
                        return 'BATTLE'
                elif event.key == pygame.K_RIGHT and (grid[player_pos[1]][player_pos[0] + 1] in [1, 2, 3] or (grid[player_pos[1]][player_pos[0] + 1] == 4 and unlocked)):
                    player_pos[0] += 1
                    player_idle = player_right
                    if battleProbability() == 1:
                        fade()
                        return 'BATTLE'
                
                if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        if paused:
                            pause.draw()
                            pygame.display.flip()
                        else:
                            screen.fill('black')
                            unknown_rendered = False
                            rooms_grid = FirstDungeon.rooms1[current_room][0]
                            description = FirstDungeon.rooms1[current_room][1]
                            grid = rooms_grid
                            room_text = text_font.render(description, True, (255, 255, 255))
                            player_pos = FirstDungeon.rooms1[current_room][2]
                            current_dialogue = Dialogues.dialogue1[current_room]    
                        continue

            if paused:
                unpause, loaded_data = pause.handle_event(event)
                if unpause and loaded_data is not None:
                    paused = False
                    current_room = loaded_data['current_room']
                    player_pos = loaded_data['player_pos']
                    grid = loaded_data['grid']
                    visibility_grid = loaded_data['visibility_grid']
                    unlocked = loaded_data['unlocked']
                    unknown_rendered = loaded_data['unknown_rendered']
                    text_show = loaded_data['text_show']
                    screen.fill('black')
                    rooms_grid = FirstDungeon.rooms1[current_room][0]
                    description = FirstDungeon.rooms1[current_room][1]
                    room_text = text_font.render(description, True, (255, 255, 255))
                    current_dialogue = Dialogues.dialogue1[current_room]
                    continue
                
                elif unpause:
                    paused = False
                    screen.fill('black')
                    unknown_rendered = False
                    rooms_grid = FirstDungeon.rooms1[current_room][0]
                    description = FirstDungeon.rooms1[current_room][1]
                    grid = rooms_grid
                    room_text = text_font.render(description, True, (255, 255, 255))
                    player_pos = FirstDungeon.rooms1[current_room][2]
                    current_dialogue = Dialogues.dialogue1[current_room]
                    continue 
                
                pause.draw()
                pygame.display.flip()
                
        if paused:
            continue      
        
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if abs(x - player_pos[0]) <= visibility_radius and abs(y - player_pos[1]) <= visibility_radius:
                    visibility_grid[y][x] = True  
                    
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if visibility_grid[y][x]: 
                    if cell == 0:
                        screen.blit(wall_image, (x * cell_size, y * cell_size))
                    elif cell == 1:
                        screen.blit(floor_image, (x * cell_size, y * cell_size))
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
                text_show = False
                unlocked = False
                unknown_rendered = False
                rooms_grid = FirstDungeon.rooms1[current_room]
                description = FirstDungeon.rooms1[current_room][1]
                grid = rooms_grid[0]
                visibility_grid = [[False for _ in row] for row in grid]
                room_text = text_font.render(description, True, (255, 255, 255))
                player_pos = FirstDungeon.rooms1[current_room][2]
                current_dialogue = Dialogues.dialogue1[current_room]
            else:
                running = False
            
        pygame.display.flip()
        
        pygame.time.Clock().tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()