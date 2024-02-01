import pygame
import os
import subprocess
import sys
import pygame.gfxdraw
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Interminable - Intro")

WIDTH, HEIGHT = 1270, 720
FPS = 60

pygame.mixer.music.load("ost/Beckon of the Grave.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(50)
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))

start_screen_image = pygame.image.load('img/intro/bgintro.png')
image_surface = pygame.image.load('img/intro/introbutton.png')

font = pygame.font.Font("fonts/Oswald.ttf", 40) 

text_surface = font.render('Press Any Key to Continue', True, (0, 0, 0))

text_width, text_height = text_surface.get_size()

image_rect = image_surface.get_rect(center=(WIDTH / 2, HEIGHT - image_surface.get_height() / 2 - 325))

def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners '''
    pygame.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2*corner_radius))
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

running = True
while running:
            
    screen.blit(start_screen_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.display.get_init():
        for alpha in range(0, 255, 5):
            image_surface.set_alpha(alpha)
            # rect = pygame.Rect(image_rect.left + 225, image_rect.top, image_rect.width - 450, text_height - 10)
            # draw_rounded_rect(screen, rect, (255, 255, 255), 20)
            screen.blit(image_surface, image_rect)
            pygame.display.flip()
            pygame.time.delay(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                        fade_surface = pygame.Surface((WIDTH, HEIGHT))
                        fade_surface.fill((0, 0, 0))

                        for alpha in range(0, 300, 2):
                            fade_surface.set_alpha(alpha) 
                            screen.blit(fade_surface, (0, 0)) 
                            pygame.display.flip() 
                            pygame.time.delay(10)

                        running = False
                        pygame.mixer.music.stop()
                        pygame.display.quit() 
                        subprocess.call(['python', 'main/battle/battle.py'])
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    fade_surface = pygame.Surface((WIDTH, HEIGHT))
                    fade_surface.fill((0, 0, 0))

                    for alpha in range(0, 300, 2):
                        fade_surface.set_alpha(alpha) 
                        screen.blit(fade_surface, (0, 0)) 
                        pygame.display.flip() 
                        pygame.time.delay(10)

                    running = False
                    pygame.mixer.music.stop()
                    pygame.display.quit() 
                    subprocess.call(['python', 'main/battle/battle.py'])
                    
                    

        screen.blit(image_surface, image_rect)

        pygame.display.flip()

    pygame.time.Clock().tick(FPS)

pygame.quit()