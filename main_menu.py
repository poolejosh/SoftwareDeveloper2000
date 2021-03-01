import os
import pygame
from button import Button

WHITE = (255, 255, 255)

class MainMenu(pygame.Rect):
    WIDTH, HEIGHT = 512, 512
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "ui", "background.png"))

    def __init__(self, left, top, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGE, (width, height))
        self.header_font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), 20)
        self.header = self.header_font.render("Software Developer 2000", False, WHITE)
        self.buttons = [
            Button(81, 100, font_size=40, label="Start Game")
        ]

