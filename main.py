import pygame
import os
import sys
import random
from loguru import logger

from main_menu import MainMenu
from hideout import Hideout
from develop import Develop
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

def draw_main_menu(main_menu):
    WIN.blit(main_menu.background, (main_menu.x, main_menu.y))
    WIN.blit(main_menu.header, (100, 10))
    
    for button in main_menu.buttons:
        WIN.blit(button.display, (button.x, button.y))
        label = button.font.render(button.label, False, BLACK)
        WIN.blit(label, (button.x + 50, button.y + 40))
    pygame.display.update()

def draw_hideout(hideout):
    WIN.blit(hideout.background, (hideout.x, hideout.y))
    WIN.blit(hideout.header, (210, 10))

    user_title = hideout.progress_font.render("Users:", False, BLACK)
    WIN.blit(user_title, (53, 60))
    WIN.blit(hideout.progress_bar, (53, 85))
    users_progress = pygame.transform.scale(hideout.PROGRESS_FILL_IMAGE, (hideout.users * 4, 24))
    WIN.blit(users_progress, (56, 88))

    user_title = hideout.progress_font.render("Reputation:", False, BLACK)
    WIN.blit(user_title, (53, 125))
    WIN.blit(hideout.progress_bar, (53, 150))
    rep_progress = pygame.transform.scale(hideout.PROGRESS_FILL_IMAGE, (hideout.reputation * 4, 24))
    WIN.blit(rep_progress, (56, 153))

    for button in hideout.buttons:
        WIN.blit(button.display, (button.x, button.y))
        label = button.font.render(button.label, False, BLACK)
        WIN.blit(label, (button.x + 25, button.y + 20))
    pygame.display.update()

    pygame.display.update()

def draw_develop_level(player, virus, develop):
    WIN.blit(develop.background, (0, 0))

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
    hideout = Hideout(0, 0)
    develop = Develop(0, 0)
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
                            mode = HIDEOUT
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 3.wav"))
                            pygame.mixer.music.play(-1)

            draw_main_menu(main_menu)

        elif mode == HIDEOUT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if hideout.buttons[0].mouse_on_button(mouse_pos):
                            mode = DEVELOP
                            pygame.mixer.music.load(os.path.join("music", "Ludum Dare 32 - Track 1.wav"))
                            pygame.mixer.music.play(-1)
                    
            draw_hideout(hideout)

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

            develop.set_background(tick)

            draw_develop_level(player, virus, develop)

            if tick < 59:
                tick += 1
            else:
                tick = 0
    
    pygame.quit()

if __name__ == "__main__":
    main()
