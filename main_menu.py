import os
import pygame
from button import Button

class MainMenu(pygame.Rect):
    WIDTH, HEIGHT = 512, 512
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "ui", "main_menu.png"))

    def __init__(self, left, top, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGE, (width, height))
        self.buttons = [
            Button(81, 100, font_size=40, label="Start Game")
        ]

