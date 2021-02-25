import pygame
import os
import sys
import random
from loguru import logger

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
VEL = 3
VIRUS_VEL = 1

COMPUTER_SPRITE_WIDTH, COMPUTER_SPRITE_HEIGHT = 64, 64
VIRUS_SPRITE_WIDTH, VIRUS_SPRITE_HEIGHT = 48, 48
CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT = 64, 64

COMPUTER_SPRITE_IMAGE_L = pygame.image.load(os.path.join("images", "sprites", "computer_sprite_l.png"))
COMPUTER_SPRITE_IMAGE_R = pygame.image.load(os.path.join("images", "sprites", "computer_sprite_r.png"))
COMPUTER_SPRITE_L = pygame.transform.scale(COMPUTER_SPRITE_IMAGE_L, (COMPUTER_SPRITE_WIDTH, COMPUTER_SPRITE_HEIGHT))
COMPUTER_SPRITE_R = pygame.transform.scale(COMPUTER_SPRITE_IMAGE_R, (COMPUTER_SPRITE_WIDTH, COMPUTER_SPRITE_HEIGHT))

CLOSE_ATTACK_IMAGES = [
    pygame.image.load(os.path.join("images", "fx", "FX003_01.png")),
    pygame.image.load(os.path.join("images", "fx", "FX003_02.png")),
    pygame.image.load(os.path.join("images", "fx", "FX003_03.png")),
    pygame.image.load(os.path.join("images", "fx", "FX003_04.png")),
    pygame.image.load(os.path.join("images", "fx", "FX003_05.png"))
]
CLOSE_ATTACK = [
    pygame.transform.scale(CLOSE_ATTACK_IMAGES[0], (CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)),
    pygame.transform.scale(CLOSE_ATTACK_IMAGES[1], (CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)),
    pygame.transform.scale(CLOSE_ATTACK_IMAGES[2], (CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)),
    pygame.transform.scale(CLOSE_ATTACK_IMAGES[3], (CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)),
    pygame.transform.scale(CLOSE_ATTACK_IMAGES[4], (CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT))
]

VIRUS_SPRITE_IMAGE = pygame.image.load(os.path.join("images", "sprites", "virus_sprite.png"))
VIRUS_SPRITE = pygame.transform.scale(VIRUS_SPRITE_IMAGE, (VIRUS_SPRITE_WIDTH, VIRUS_SPRITE_HEIGHT))


def draw_main_menu():
    WIN.fill(RED)
    pygame.display.update()

def draw_hideout():
    WIN.fill(GREEN)
    pygame.display.update()

def draw_develop_level(player, player_left, virus, close_attack=None):
    WIN.fill(WHITE)
    if player_left:
        player_sprite = COMPUTER_SPRITE_L
    else:
        player_sprite = COMPUTER_SPRITE_R

    WIN.blit(player_sprite, (player.x, player.y)) # draw a surface onto window
    
    WIN.blit(VIRUS_SPRITE, (virus.x, virus.y))
    
    if close_attack:
        WIN.blit(close_attack[0], (close_attack[1].x, close_attack[1].y))

    pygame.display.update()

def handle_player_movement(keys_pressed, player, player_left):
    if keys_pressed[pygame.K_a] and player.x - VEL > 0: # LEFT
        player.x -= VEL
        player_left = True
    if keys_pressed[pygame.K_d] and player.x + player.width + VEL < WIDTH: # RIGHT
        player.x += VEL
        player_left = False
    if keys_pressed[pygame.K_w] and player.y - VEL > 0: # UP
        player.y -= VEL
    if keys_pressed[pygame.K_s] and player.y + player.height + VEL < HEIGHT: # DOWN
        player.y += VEL

    return player_left

def find_mouse_direction_relative_to_player(player):
    mouse_pos = pygame.mouse.get_pos()

    if mouse_pos[0] < player.x and mouse_pos[1] > player.y and mouse_pos[1] < player.y + player.height : # LEFT
        direction = WEST
    elif mouse_pos[0] > player.x + player.width and mouse_pos[1] > player.y and mouse_pos[1] < player.y + player.height : # RIGHT
        direction  = EAST
    elif mouse_pos[1] < player.y and mouse_pos[0] > player.x and mouse_pos[0] < player.x + player.width: # UP
        direction = NORTH
    elif mouse_pos[1] > player.y + player.height and mouse_pos[0] > player.x and mouse_pos[0] < player.x + player.width: # DOWN
        direction = SOUTH
    elif mouse_pos[0] < player.x and mouse_pos[1] < player.y:
        direction = NW
    elif mouse_pos[0] > player.x + player.width and mouse_pos[1] < player.y:
        direction = NE
    elif mouse_pos[1] > player.y + player.height and mouse_pos[0] < player.x:
        direction = SW
    elif mouse_pos[1] > player.y + player.height and mouse_pos[0] > player.x + player.width:
        direction = SE
    else:
        direction = None
    
    return direction

def handle_close_attack(player, tick, do_close_attack):
    starting_tick = do_close_attack[1]
    direction = do_close_attack[2]

    if tick > starting_tick and abs(tick - starting_tick) < 30:
        if tick < starting_tick + 6:
            attack_frame = CLOSE_ATTACK[0]
        elif tick >= starting_tick + 6 and tick < starting_tick + 12:
            attack_frame = CLOSE_ATTACK[1]
        elif tick >= starting_tick + 12 and tick < starting_tick + 18:
            attack_frame = CLOSE_ATTACK[2]
        elif tick >= starting_tick + 18 and tick < starting_tick + 24:
            attack_frame = CLOSE_ATTACK[3]
        else:
            attack_frame = CLOSE_ATTACK[4]

    elif tick < starting_tick and tick + abs(60 - starting_tick) < 30:
        if tick + abs(60 - starting_tick) >= 24:
            attack_frame = CLOSE_ATTACK[4]
        elif tick + abs(60 - starting_tick) < 24 and tick + abs(60 - starting_tick) >= 18:
            attack_frame = CLOSE_ATTACK[3]
        elif tick + abs(60 - starting_tick) < 18 and tick + abs(60 - starting_tick) >= 12:
            attack_frame = CLOSE_ATTACK[2]
        elif tick + abs(60 - starting_tick) < 12 and tick + abs(60 - starting_tick) >= 6:
            attack_frame = CLOSE_ATTACK[1]
        else:
            attack_frame = CLOSE_ATTACK[0]

    else:
        do_close_attack[0] = False
    
    if do_close_attack[0]:
        if direction == WEST:
            attack_frame = pygame.transform.rotate(attack_frame, 90)
            close_attack = pygame.Rect(player.x - CLOSE_ATTACK_WIDTH, player.y, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        elif direction == EAST:
            attack_frame = pygame.transform.rotate(attack_frame, 270)
            close_attack = pygame.Rect(player.x + player.width, player.y, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        elif direction == NORTH:
            close_attack = pygame.Rect(player.x, player.y - CLOSE_ATTACK_HEIGHT, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        elif direction == SOUTH:
            attack_frame = pygame.transform.rotate(attack_frame, 180)
            close_attack = pygame.Rect(player.x, player.y + player.height, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        elif direction == NW:
            attack_frame = pygame.transform.rotate(attack_frame, 45)
            close_attack = pygame.Rect(player.x - CLOSE_ATTACK_WIDTH, player.y - CLOSE_ATTACK_HEIGHT, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        elif direction == NE:
            attack_frame = pygame.transform.rotate(attack_frame, 315)
            close_attack = pygame.Rect(player.x + player.width - 20, player.y - CLOSE_ATTACK_HEIGHT, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        elif direction == SW:
            attack_frame = pygame.transform.rotate(attack_frame, 135)
            close_attack = pygame.Rect(player.x - CLOSE_ATTACK_WIDTH, player.y + player.height - 20, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)
        else:
            attack_frame = pygame.transform.rotate(attack_frame, 225)
            close_attack = pygame.Rect(player.x + player.width - 20, player.y + player.height - 20, CLOSE_ATTACK_WIDTH, CLOSE_ATTACK_HEIGHT)

        return do_close_attack, [attack_frame, close_attack]

    else:
        return do_close_attack, None


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
    logger.debug("Game Running!")
    player = pygame.Rect(WIDTH/2 - COMPUTER_SPRITE_WIDTH/2, HEIGHT/2 - COMPUTER_SPRITE_HEIGHT/2, COMPUTER_SPRITE_WIDTH, COMPUTER_SPRITE_HEIGHT)
    close_attack = None
    virus = pygame.Rect(400, 300, VIRUS_SPRITE_WIDTH, VIRUS_SPRITE_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    tick = 0
    mode = DEVELOP # current game mode
    player_left = False # direction player is facing
    do_close_attack = [False, 0, None] # do close attack, starting tick, and direction

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
                    if mouse_button[0] and do_close_attack[0] == False:
                        direction = find_mouse_direction_relative_to_player(player)
                        
                        if direction:
                            do_close_attack = [True, tick-1, direction]
                            logger.debug("Do close attack! Direction = {}".format(direction))

            
            keys_pressed = pygame.key.get_pressed()
            player_left = handle_player_movement(keys_pressed, player, player_left)
            if (tick == 0 or tick == FPS/2):
                if random.randint(0,1) == 0:
                    virus_direction = generate_random_direction()
                else:
                    virus_direction = None

            if do_close_attack[0]:
                do_close_attack, close_attack = handle_close_attack(player, tick, do_close_attack)
            
            handle_virus_movement(virus_direction, virus)

            draw_develop_level(player, player_left, virus, close_attack)
            if tick < 59:
                tick += 1
            else:
                tick = 0
    
    pygame.quit()

if __name__ == "__main__":
    main()
