import os
import pygame
from other.button import Button

pygame.font.init()

class MainMenuButton(Button):
    WIDTH, HEIGHT = 350, 150
    IMAGE = pygame.image.load(os.path.join("assets", "images", "ui", "main_menu_button.png"))

    def __init__(self, left, top, label, font_size=40, width=WIDTH, height=HEIGHT):
        Button.__init__(self, left, top, label, font_size, width, height)
        self.display = pygame.transform.scale(self.IMAGE, (width, height))
