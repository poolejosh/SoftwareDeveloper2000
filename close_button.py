import os
import pygame
from button import Button

BLACK = (0, 0, 0)

class CloseButton(Button):
    WIDTH, HEIGHT = 30, 30
    IMAGE = pygame.image.load(os.path.join("images", "ui", "close_button.png"))

    def __init__(self, left, top, label="X", font_size=16, width=WIDTH, height=HEIGHT):
        Button.__init__(self, left, top, label, font_size, width, height)
        self.display = pygame.transform.scale(self.IMAGE, (width, height))
