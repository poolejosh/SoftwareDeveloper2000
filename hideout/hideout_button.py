import os
import pygame
from other.button import Button

# pygame.font.init() TODO: remove?

class HideoutButton(Button):
    WIDTH, HEIGHT = 200, 90
    IMAGE = pygame.image.load(os.path.join("assets", "images", "ui", "hideout_button.png"))

    def __init__(self, left, top, label, font_size=24, width=WIDTH, height=HEIGHT):
        Button.__init__(self, left, top, label, font_size, width, height)
        self.display = pygame.transform.scale(self.IMAGE, (width, height))
