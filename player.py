import os
import pygame
from directed_attack import DirectedAttack
from aoe_attack import AoeAttack

WIDTH, HEIGHT = 512, 512 # TODO: get from screen/window class
WEST, EAST, NORTH, SOUTH, NW, NE, SW, SE = "WEST", "EAST", "NORTH", "SOUTH", "NW", "NE", "SW", "SE"
VEL = 3

class Player(pygame.Rect):
    SPRITE_IMATE_L = pygame.image.load(os.path.join("images", "sprites", "computer_sprite_l.png"))
    SPRITE_IMAGE_R = pygame.image.load(os.path.join("images", "sprites", "computer_sprite_r.png"))

    def __init__(self, left, top, width, height, facing_left):
        pygame.Rect.__init__(self, left, top, width, height)
        self.facing_left = facing_left
        self.sprite_l = pygame.transform.scale(self.SPRITE_IMATE_L, (width, height))
        self.sprite_r = pygame.transform.scale(self.SPRITE_IMAGE_R, (width, height))

        self.directed_attack = DirectedAttack(left, top)
        self.doing_directed_attack = False

        self.aoe_attack = AoeAttack(left - 32, top - 32)
        self.doing_aoe_attack = False

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.x - VEL > 0: # LEFT
            self.x -= VEL
            self.facing_left = True
        if keys_pressed[pygame.K_d] and self.x + self.width + VEL < WIDTH: # RIGHT
            self.x += VEL
            self.facing_left = False
        if keys_pressed[pygame.K_w] and self.y - VEL > 0: # UP
            self.y -= VEL
        if keys_pressed[pygame.K_s] and self.y + self.height + VEL < HEIGHT: # DOWN
            self.y += VEL

    def mouse_direction_relative_to_player(self, mouse_pos):
        if mouse_pos[0] < self.x and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
            direction = WEST
        elif mouse_pos[0] > self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
            direction  = EAST
        elif mouse_pos[1] < self.y and mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            direction = NORTH
        elif mouse_pos[1] > self.y + self.height and mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            direction = SOUTH
        elif mouse_pos[0] < self.x and mouse_pos[1] < self.y:
            direction = NW
        elif mouse_pos[0] > self.x + self.width and mouse_pos[1] < self.y:
            direction = NE
        elif mouse_pos[1] > self.y + self.height and mouse_pos[0] < self.x:
            direction = SW
        elif mouse_pos[1] > self.y + self.height and mouse_pos[0] > self.x + self.width:
            direction = SE
        else:
            direction = None
        
        return direction
    
    def resolve_directed_attack(self, tick):
        self.directed_attack.determine_frame(tick)
        if self.directed_attack.frame:
            if self.directed_attack.direction == WEST:
                self.directed_attack.rotate_frame(90)
                self.directed_attack.x = self.x - self.directed_attack.width
                self.directed_attack.y = self.y
            elif self.directed_attack.direction == EAST:
                self.directed_attack.rotate_frame(270)
                self.directed_attack.x = self.x + self.width
                self.directed_attack.y = self.y
            elif self.directed_attack.direction == NORTH:
                self.directed_attack.x = self.x
                self.directed_attack.y = self.y - self.directed_attack.height
            elif self.directed_attack.direction == SOUTH:
                self.directed_attack.rotate_frame(180)
                self.directed_attack.x = self.x
                self.directed_attack.y = self.y + self.height
            elif self.directed_attack.direction == NW:
                self.directed_attack.rotate_frame(45)
                self.directed_attack.x = self.x - self.directed_attack.width
                self.directed_attack.y = self.y - self.directed_attack.height
            elif self.directed_attack.direction == NE:
                self.directed_attack.rotate_frame(315)
                self.directed_attack.x = self.x + self.width - 20 # manually changed to be visually closer to player
                self.directed_attack.y = self.y - self.directed_attack.height
            elif self.directed_attack.direction == SW:
                self.directed_attack.rotate_frame(135)
                self.directed_attack.x = self.x - self.directed_attack.width
                self.directed_attack.y = self.y + self.height - 20
            else:
                self.directed_attack.rotate_frame(225)
                self.directed_attack.x = self.x + self.width - 20
                self.directed_attack.y = self.y + self.height - 20

        else:
            self.doing_directed_attack = False

    def resolve_aoe_attack(self, tick):
        self.aoe_attack.determine_frame(tick)
        if self.aoe_attack.frame:
            self.aoe_attack.x = self.x - 32
            self.aoe_attack.y = self.y - 32
        else:
            self.doing_aoe_attack = False