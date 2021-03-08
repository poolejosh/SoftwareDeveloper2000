import os
import pygame
from close_button import CloseButton

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class PopUp(pygame.Rect):
    WIDTH, HEIGHT = 384, 384
    BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "ui", "popup_background.png"))

    def __init__(self, left, top, header_text, body_file, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGE, (width, height))
        self.header_font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), 20)
        self.header = self.header_font.render(header_text, False, WHITE)
        
        self.body_font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), 14)
        with open(body_file, "r") as f:
            self.body_text = f.read().replace("\n", " ")
        
        self.body_rect = pygame.Rect(self.x + 15, self.y + 60, self.width - 20, self.height - 70)

        self.close_button = CloseButton(self.x + self.width - 42, self.y + 15)
