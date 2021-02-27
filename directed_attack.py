import os
import pygame
from attack import Attack

class DirectedAttack(Attack):
    DIRECTED_ATTACK_WIDTH, DIRECTED_ATTACK_HEIGHT = 64, 64
    DIRECTED_ATTACK_IMAGES = [
        pygame.image.load(os.path.join("images", "fx", "directed_attack", "0.png")),
        pygame.image.load(os.path.join("images", "fx", "directed_attack", "1.png")),
        pygame.image.load(os.path.join("images", "fx", "directed_attack", "2.png")),
        pygame.image.load(os.path.join("images", "fx", "directed_attack", "3.png")),
        pygame.image.load(os.path.join("images", "fx", "directed_attack", "4.png")),
    ]
    DIRECTED_ATTACK = [
        pygame.transform.scale(DIRECTED_ATTACK_IMAGES[0], (DIRECTED_ATTACK_WIDTH, DIRECTED_ATTACK_HEIGHT)),
        pygame.transform.scale(DIRECTED_ATTACK_IMAGES[1], (DIRECTED_ATTACK_WIDTH, DIRECTED_ATTACK_HEIGHT)),
        pygame.transform.scale(DIRECTED_ATTACK_IMAGES[2], (DIRECTED_ATTACK_WIDTH, DIRECTED_ATTACK_HEIGHT)),
        pygame.transform.scale(DIRECTED_ATTACK_IMAGES[3], (DIRECTED_ATTACK_WIDTH, DIRECTED_ATTACK_HEIGHT)),
        pygame.transform.scale(DIRECTED_ATTACK_IMAGES[4], (DIRECTED_ATTACK_WIDTH, DIRECTED_ATTACK_HEIGHT))
    ]
    
    def __init__(self, left, top, width=DIRECTED_ATTACK_WIDTH, height=DIRECTED_ATTACK_HEIGHT):
        Attack.__init__(self, left, top, width, height)
        self.started = False
        self.starting_tick = None
        self.frame = None
        self.direction = None
        self.hitbox = pygame.Rect(left, top, width, height)

    def set_frame(self, frame_index):
        self.frame = self.DIRECTED_ATTACK[frame_index]

    def determine_frame(self, tick):
        if tick == self.starting_tick and self.started == False:
            self.set_frame(0)
            self.started = True
        elif tick > self.starting_tick and abs(tick - self.starting_tick) < 30:
            if tick < self.starting_tick + 6:
                self.set_frame(0)
            elif tick >= self.starting_tick + 6 and tick < self.starting_tick + 12:
                self.set_frame(1)
            elif tick >= self.starting_tick + 12 and tick < self.starting_tick + 18:
                self.set_frame(2)
            elif tick >= self.starting_tick + 18 and tick < self.starting_tick + 24:
                self.set_frame(3)
            else:
                self.set_frame(4)

        elif tick < self.starting_tick and tick + abs(60 - self.starting_tick) < 30:
            if tick + abs(60 - self.starting_tick) >= 24:
                self.set_frame(4)
            elif tick + abs(60 - self.starting_tick) < 24 and tick + abs(60 - self.starting_tick) >= 18:
                self.set_frame(3)
            elif tick + abs(60 - self.starting_tick) < 18 and tick + abs(60 - self.starting_tick) >= 12:
                self.set_frame(2)
            elif tick + abs(60 - self.starting_tick) < 12 and tick + abs(60 - self.starting_tick) >= 6:
                self.set_frame(1)
            else:
                self.set_frame(0)
        
        else:
            self.frame = None
            self.started = False

    def rotate_frame(self, degrees):
        self.frame = pygame.transform.rotate(self.frame, degrees)

    def update_location(self, x, y):
        self.x = x
        self.y = y

    def update_hitbox(self, x, y):
        self.hitbox.x = x
        self.hitbox.y = y
