import os
import random
import pygame
from enemy import Enemy

from common import logger

WIDTH, HEIGHT = 512, 512 # TODO: get from screen/window class
WEST, EAST, NORTH, SOUTH, NW, NE, SW, SE = "WEST", "EAST", "NORTH", "SOUTH", "NW", "NE", "SW", "SE"
DIRECTIONS = [NW, NORTH, NE, EAST, SE, SOUTH, SW, WEST, NW, NORTH, NE, EAST]
VEL = 1

class VirusEnemy(Enemy):
    VIRUS_WIDTH, VIRUS_HEIGHT = 48, 48
    VIRUS_SPRITE_IMAGE = pygame.image.load(os.path.join("images", "sprites", "virus_sprite.png"))

    def __init__(self, left, top, width=VIRUS_WIDTH, height=VIRUS_HEIGHT):
        Enemy.__init__(self, left, top, width, height)
        self.sprite = pygame.transform.scale(self.VIRUS_SPRITE_IMAGE, (width, height))
        self.direction = self.generate_random_direction()

        self.hitbox = pygame.Rect(left, top, width, height)

    @staticmethod
    def generate_random_direction():
        return DIRECTIONS[random.randint(0, 7)]

    def touching_wall(self):
        if self.x <= VEL:
            wall = WEST
        elif WIDTH - (self.x + self.width) <= VEL:
            wall = EAST
        elif self.y <= VEL:
            wall = NORTH
        elif HEIGHT - (self.y + self.height) <= VEL:
            wall = SOUTH
        else:
            wall = None
        
        return wall

    def change_direction(self):
        wall = self.touching_wall()
        if random.randint(0, 3) == 3:
            self.direction = None
        elif wall:
            rand = random.randint(1, 5)
            if wall == NORTH:
                rand += 2
            elif wall == EAST:
                rand += 4
            elif wall == SOUTH:
                rand += 6
            
            self.direction = DIRECTIONS[rand]
        else:
            rand = random.randint(0, 2)
            if self.direction == None:
                self.generate_random_direction()
            elif self.direction == NE:
                rand += 7
            else:
                rand += DIRECTIONS.index(self.direction) - 1
            
            self.direction = DIRECTIONS[rand]
    
    def handle_movement(self):
        if self.direction == WEST and self.x - VEL > 0:
            self.x -= VEL
        if self.direction == EAST and self.x + self.width + VEL < WIDTH:
            self.x += VEL
        if self.direction == NORTH and self.y - VEL > 0:
            self.y -= VEL
        if self.direction == SOUTH and self.y + self.height + VEL < HEIGHT:
            self.y += VEL
        if self.direction == NW and self.y - VEL > 0 and self.x - VEL > 0:
            self.x -= VEL
            self.y -= VEL
        if self.direction == NE and self.y - VEL > 0 and self.x + self.width + VEL < WIDTH:
            self.x += VEL
            self.y -= VEL
        if self.direction == SW and self.y + self.height + VEL < HEIGHT and self.x - VEL > 0:
            self.x -= VEL
            self.y += VEL
        if self.direction == SE and self.y + self.height + VEL < HEIGHT and self.x + self.width + VEL < WIDTH:
            self.x += VEL
            self.y += VEL

        
        self.update_hitbox()
    
    def update_hitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y