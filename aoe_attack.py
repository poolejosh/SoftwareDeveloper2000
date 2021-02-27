import os
import pygame
from attack import Attack

class AoeAttack(Attack):
    AOE_ATTACK_WIDTH, AOE_ATTACK_HEIGHT = 128, 128

    def __init__(self, left, top, width=AOE_ATTACK_WIDTH, height=AOE_ATTACK_HEIGHT):
        Attack.__init__(self, left, top, width, height)
        self.started = False
        self.starting_tick = None
        self.frame = None
        self.hitbox = pygame.Rect(left+20, top+20, width-32, height-30)

    def set_frame(self, frame_index):
        frame_image = pygame.image.load(os.path.join("images", "fx", "aoe_attack", "{}.png".format(frame_index)))
        self.frame = pygame.transform.scale(frame_image, (self.AOE_ATTACK_WIDTH, self.AOE_ATTACK_HEIGHT))

    def determine_frame(self, tick):
        if tick == self.starting_tick and self.started == False:
            self.set_frame(tick)
            self.started = True
        elif tick == self.starting_tick and self.started == True:
            self.frame = None
            self.started = False
        else:
            self.set_frame(tick)

    def update_location(self, x, y):
        self.x = x
        self.y = y
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.x = self.x + 20
        self.hitbox.y = self.y + 20
