import os
import pygame
from button import Button

pygame.font.init()

class HideoutButton(Button):
    WIDTH, HEIGHT = 200, 90
    IMAGE = pygame.image.load(os.path.join("images", "ui", "hideout_button.png"))

    def __init__(self, left, top, font_size, label, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.display = pygame.transform.scale(self.IMAGE, (width, height))
        self.font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), font_size)
        self.label = label