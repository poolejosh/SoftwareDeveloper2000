import pygame
import os
import sys
import random
from loguru import logger

from player import Player

LOGGER_FORMAT = "<green>{time}</green> <level>{message}</level>"

logger.remove()
logger.add(sys.stdout, colorize=True, format=LOGGER_FORMAT)

WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Software Developer 2000")

MAIN_MENU = "MAIN_MENU"
HIDEOUT = "HIDEOUT"
DEVELOP = "DEVELOP"

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WEST, EAST, NORTH, SOUTH, NW, NE, SW, SE = "WEST", "EAST", "NORTH", "SOUTH", "NW", "NE", "SW", "SE"
DIRECTIONS = [WEST, EAST, NORTH, SOUTH, NW, NE, SW, SE]

FPS = 60
VIRUS_VEL = 1

PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64
VIRUS_SPRITE_WIDTH, VIRUS_SPRITE_HEIGHT = 48, 48

VIRUS_SPRITE_IMAGE = pygame.image.load(os.path.join("images", "sprites", "virus_sprite.png"))
VIRUS_SPRITE = pygame.transform.scale(VIRUS_SPRITE_IMAGE, (VIRUS_SPRITE_WIDTH, VIRUS_SPRITE_HEIGHT))

def draw_main_menu():
    WIN.fill(RED)
    pygame.display.update()

def draw_hideout():
    WIN.fill(GREEN)
    pygame.display.update()

def draw_develop_level(player, virus):
    WIN.fill(WHITE)
    if player.facing_left:
        WIN.blit(player.sprite_l, (player.x, player.y))
    else:
        WIN.blit(player.sprite_r, (player.x, player.y))
    
    WIN.blit(VIRUS_SPRITE, (virus.x, virus.y))
    
    if player.doing_directed_attack:
        WIN.blit(player.directed_attack.frame, (player.directed_attack.x, player.directed_attack.y))

    pygame.display.update()


def generate_random_direction():
    return DIRECTIONS[random.randint(0, 3)]

def handle_virus_movement(direction, virus):
    if direction == WEST and virus.x - VIRUS_VEL > 0: # LEFT
        virus.x -= VIRUS_VEL
    if direction == EAST and virus.x + virus.width + VIRUS_VEL < WIDTH: # RIGHT
        virus.x += VIRUS_VEL
    if direction == NORTH and virus.y - VIRUS_VEL > 0: # UP
        virus.y -= VIRUS_VEL
    if direction == SOUTH and virus.y + virus.height + VIRUS_VEL < HEIGHT: # DOWN
        virus.y += VIRUS_VEL

def main():
    logger.debug("Game is Running!")
    player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT, False)
    virus = pygame.Rect(400, 300, VIRUS_SPRITE_WIDTH, VIRUS_SPRITE_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    tick = 0
    mode = DEVELOP # current game mode

    virus_direction = None
    while run:
        clock.tick(FPS) # limit game loop to 60 FPS 

        if mode == MAIN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            draw_main_menu()

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
                    if mouse_button[0] and player.doing_directed_attack == False:
                        mouse_pos = pygame.mouse.get_pos()
                        direction = player.mouse_direction_relative_to_player(mouse_pos)
                        
                        if direction:
                            player.doing_directed_attack = True
                            player.directed_attack.direction = direction
                            player.directed_attack.starting_tick = tick - 1

            
            keys_pressed = pygame.key.get_pressed()
            player.handle_movement(keys_pressed)
            if (tick == 0 or tick == FPS/2):
                if random.randint(0,1) == 0:
                    virus_direction = generate_random_direction()
                else:
                    virus_direction = None

            if player.doing_directed_attack:
                player.resolve_directed_attack(tick)
            
            handle_virus_movement(virus_direction, virus)

            draw_develop_level(player, virus)
            if tick < 59:
                tick += 1
            else:
                tick = 0
    
    pygame.quit()

if __name__ == "__main__":
    main()
