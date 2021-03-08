import os
import pygame

class Develop(pygame.Rect):
    WIDTH, HEIGHT = 512, 512
    BACKGROUND_IMAGES = [
    pygame.image.load(os.path.join("images", "matrix_background", "0.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "1.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "2.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "3.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "4.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "5.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "6.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "7.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "8.png")),
    pygame.image.load(os.path.join("images", "matrix_background", "9.png")),
    ]
    HEALTH_BAR_IMAGE = pygame.image.load(os.path.join("images", "ui", "health_bar.png"))
    HEALTH_FILL_IMAGE = pygame.image.load(os.path.join("images", "ui", "health_fill.png"))


    def __init__(self, left, top, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[0], (width, height))
        self.health_bar = pygame.transform.scale(self.HEALTH_BAR_IMAGE, (406, 20))

    def set_background(self, tick):
        if tick < 6:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[0], (self.width, self.height))
        elif tick >= 6 and tick < 12:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[1], (self.width, self.height))
        elif tick >= 12 and tick < 18:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[2], (self.width, self.height))
        elif tick >= 18 and tick < 24:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[3], (self.width, self.height))
        elif tick >= 24 and tick < 30:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[4], (self.width, self.height))
        elif tick >= 30 and tick < 36:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[5], (self.width, self.height))
        elif tick >= 36 and tick < 42:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[6], (self.width, self.height))
        elif tick >= 42 and tick < 48:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[7], (self.width, self.height))
        elif tick >= 48 and tick < 54:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[8], (self.width, self.height))
        else:
            self.background = pygame.transform.scale(self.BACKGROUND_IMAGES[9], (self.width, self.height))
