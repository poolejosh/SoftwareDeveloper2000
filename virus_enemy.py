import os
import random
import pygame
from enemy import Enemy

WIDTH, HEIGHT = 512, 512 # TODO: get from screen/window class
WEST, EAST, NORTH, SOUTH, NW, NE, SW, SE = "WEST", "EAST", "NORTH", "SOUTH", "NW", "NE", "SW", "SE"
DIRECTIONS = [WEST, EAST, NORTH, SOUTH, NW, NE, SW, SE]
VEL = 1

class VirusEnemy(Enemy):
    VIRUS_WIDTH, VIRUS_HEIGHT = 48, 48
    VIRUS_SPRITE_IMAGE = pygame.image.load(os.path.join("images", "sprites", "virus_sprite.png"))

    def __init__(self, left, top, width=VIRUS_WIDTH, height=VIRUS_HEIGHT):
        Enemy.__init__(self, left, top, width, height)
        self.sprite = pygame.transform.scale(self.VIRUS_SPRITE_IMAGE, (width, height))

        self.hitbox = pygame.Rect(left, top, width, height)

    @staticmethod
    def generate_random_direction():
        return DIRECTIONS[random.randint(0, 3)]

    def handle_movement(self, direction):
        if direction == WEST and self.x - VEL > 0:
            self.x -= VEL
        if direction == EAST and self.x + self.width + VEL < WIDTH:
            self.x += VEL
        if direction == NORTH and self.y - VEL > 0:
            self.y -= VEL
        if direction == SOUTH and self.y + self.height + VEL < HEIGHT:
            self.y += VEL
        
        self.update_hitbox()
    
    def update_hitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y