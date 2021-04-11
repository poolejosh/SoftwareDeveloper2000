import os
import pygame

WHITE = (255, 255, 255)

class Hideout(pygame.Rect):
    WIDTH, HEIGHT = 512, 512
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "images", "ui", "background.png"))

    
    def __init__(self, left, top, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGE, (width, height))
        self.header_font = pygame.font.Font(os.path.join("assets", "fonts", "M_8pt.ttf"), 20)
        self.header = self.header_font.render("Level 0", False, WHITE)

        with open(os.path.join("assets", "popup_info", "vuln.txt"), "r") as f:
            self.body_text = f.read().replace("\n", " ")
        
        self.body_font = pygame.font.Font(os.path.join("assets", "fonts", "M_8pt.ttf"), 18)
        self.body_rect = pygame.Rect(self.x + 15, self.y + 60, self.width - 20, self.height / 2)