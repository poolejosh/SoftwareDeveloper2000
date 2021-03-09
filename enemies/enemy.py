import pygame

class Enemy(pygame.Rect):
    def __init__(self, left, top, width, height):
        pygame.Rect.__init__(self, left, top, width, height)