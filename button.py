import os
import pygame

pygame.font.init()

class Button(pygame.Rect):
    WIDTH, HEIGHT = 350, 150
    IMAGE = pygame.image.load(os.path.join("images", "ui", "main_menu_button.png"))

    def __init__(self, left, top, font_size, label, width=WIDTH, height=HEIGHT):
        pygame.Rect.__init__(self, left, top, width, height)
        self.display = pygame.transform.scale(self.IMAGE, (width, height))
        self.font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), font_size)
        self.label = label

    def mouse_on_button(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if mouse_x > self.x and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height:
            return True
        else:
            return False

