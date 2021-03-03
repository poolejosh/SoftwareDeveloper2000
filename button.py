import os
import pygame

BLACK = (0, 0, 0)

class Button(pygame.Rect):
    def __init__(self, left, top, label, font_size, width, height):
        pygame.Rect.__init__(self, left, top, width, height)
        self.font = pygame.font.Font(os.path.join("fonts", "M_8pt.ttf"), font_size)
        self.label = self.font.render(label, False, BLACK)

    def mouse_on_button(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if mouse_x > self.x and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height:
            return True
        else:
            return False