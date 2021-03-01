import pygame
import os
import sys
import random
from loguru import logger

from main_menu import MainMenu
from player import Player
from virus_enemy import VirusEnemy

LOGGER_FORMAT = "<green>{time}</green> <level>{message}</level>"

logger.remove()
logger.add(sys.stdout, colorize=True, format=LOGGER_FORMAT)

WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Software Developer 2000")

MAIN_MENU = "MAIN_MENU"
HIDEOUT = "HIDEOUT"
DEVELOP = "DEVELOP"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

FPS = 60

PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64

BACKGROUND_IMAGES = [
    pygame.image.load(os.path.join("images", "matrix_background", "0.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "1.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "2.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "3.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "4.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "5.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "6.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "7.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "8.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "9.png")),
]

def determine_develop_background(tick):
    if tick < 6:
        background = pygame.transform.scale(BACKGROUND_IMAGES[0], (WIDTH, HEIGHT))
    elif tick >= 6 and tick < 12:
        background = pygame.transform.scale(BACKGROUND_IMAGES[1], (WIDTH, HEIGHT))
    elif tick >= 12 and tick < 18:
        background = pygame.transform.scale(BACKGROUND_IMAGES[2], (WIDTH, HEIGHT))
    elif tick >= 18 and tick < 24:
        background = pygame.transform.scale(BACKGROUND_IMAGES[3], (WIDTH, HEIGHT))
    elif tick >= 24 and tick < 30:
        background = pygame.transform.scale(BACKGROUND_IMAGES[4], (WIDTH, HEIGHT))
    elif tick >= 30 and tick < 36:
        background = pygame.transform.scale(BACKGROUND_IMAGES[5], (WIDTH, HEIGHT))
    elif tick >= 36 and tick < 42:
        background = pygame.transform.scale(BACKGROUND_IMAGES[6], (WIDTH, HEIGHT))
    elif tick >= 42 and tick < 48:
        background = pygame.transform.scale(BACKGROUND_IMAGES[7], (WIDTH, HEIGHT))
    elif tick >= 48 and tick < 54:
        background = pygame.transform.scale(BACKGROUND_IMAGES[8], (WIDTH, HEIGHT))
    else:
       background = pygame.transform.scale(BACKGROUND_IMAGES[9], (WIDTH, HEIGHT))

    return background

def draw_main_menu(main_menu):
    WIN.blit(main_menu.background, (main_menu.x, main_menu.y))
    WIN.blit(main_menu.header, (100, 10))
    
    for button in main_menu.buttons:
        WIN.blit(button.display, (button.x, button.y))
        label = button.font.render(button.label, False, BLACK)
        WIN.blit(label, (button.x + 50, button.y + 40))
    pygame.display.update()

def draw_hideout():
    WIN.fill(GREEN)
    pygame.display.update()

def draw_develop_level(player, virus, background):
    WIN.blit(background, (0, 0))

    WIN.blit(virus.sprite, (virus.x, virus.y))
    pygame.draw.rect(WIN, MAGENTA, virus.hitbox, 1)

    if player.doing_aoe_attack:
        WIN.blit(player.aoe_attack.frame, (player.aoe_attack.x, player.aoe_attack.y))
        pygame.draw.rect(WIN, BLUE, player.aoe_attack.hitbox, 1)

    if player.facing_left:
        WIN.blit(player.sprite_l, (player.x, player.y))
    else:
        WIN.blit(player.sprite_r, (player.x, player.y))
    pygame.draw.rect(WIN, RED, player.hitbox, 1)

    if player.doing_directed_attack:
        WIN.blit(player.directed_attack.frame, (player.directed_attack.x, player.directed_attack.y))
        pygame.draw.rect(WIN, GREEN, player.directed_attack.hitbox, 1)
        if player.directed_attack.hitbox.colliderect(virus.hitbox):
            pass
    
    pygame.display.update()

def main():
    logger.debug("Game is Running!")
    main_menu = MainMenu(0, 0)
    player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT, False)
    virus = VirusEnemy(400, 300)

    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 4.wav"))
    pygame.mixer.music.set_volume(0.01) # TODO: 0.1 when done
    pygame.mixer.music.play(-1)
    run = True
    tick = 0
    mode = MAIN_MENU # current game mode
    while run:
        clock.tick(FPS) # limit game loop to 60 FPS 

        if mode == MAIN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if main_menu.buttons[0].mouse_on_button(mouse_pos):
                            mode = DEVELOP # TODO: change to hideout eventually?
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 1.wav"))
                            pygame.mixer.music.play(-1)

            draw_main_menu(main_menu)

        elif mode == HIDEOUT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            draw_hideout()

        elif mode == DEVELOP:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if not player.doing_directed_attack and not player.doing_aoe_attack:
                        if mouse_button[0] and player.doing_directed_attack == False:
                            mouse_pos = pygame.mouse.get_pos()
                            direction = player.mouse_direction_relative_to_player(mouse_pos)
                            
                            if direction:
                                player.doing_directed_attack = True
                                player.directed_attack.direction = direction
                                player.directed_attack.starting_tick = tick
                        
                        elif mouse_button[2] and player.doing_aoe_attack == False:
                            player.doing_aoe_attack = True
                            player.aoe_attack.starting_tick = tick

            
            keys_pressed = pygame.key.get_pressed()
            player.handle_movement(keys_pressed)
            if (tick == 0):
                virus.change_direction()

            if player.doing_directed_attack:
                player.resolve_directed_attack(tick)
            elif player.doing_aoe_attack:
                player.resolve_aoe_attack(tick)

            virus.handle_movement()

            background = determine_develop_background(tick)

            draw_develop_level(player, virus, background)

            if tick < 59:
                tick += 1
            else:
                tick = 0
    
    pygame.quit()

if __name__ == "__main__":
    main()
