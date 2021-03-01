import os
import pygame
from hideout_button import HideoutButton

WHITE = (255, 255, 255)

class Hideout(pygame.Rect):
    WIDTH, HEIGHT = 512, 512
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "ui", "background.png"))
    PROGRESS_BAR_IMAGE = pygame.image.load(os.path.join("images", "ui", "progress_bar.png"))
    PROGRESS_FILL_IMAGE = pygame.image.load(os.path.join("images", "ui", "progress_fill.png"))
    
    def __init__(self, left, top, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGE, (width, height))
        self.header_font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), 20)
        self.header = self.header_font.render("Hideout", False, WHITE)
        self.progress_font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), 14)
        self.progress_bar = pygame.transform.scale(self.PROGRESS_BAR_IMAGE, (406, 30))
        self.buttons = [
            HideoutButton(50, 200, font_size=30, label="Develop")
        ]

        self.users = 0
        self.user_rate = 0

        self.reputation = 0
        self.rep_rate = 0
        self.dollars = 0
        self.features = []
        self.debuffs = []

    def update_users(self):
        self.users += self.user_rate
    
    def update_reputation(self):
        self.reputation += self.rep_rate
