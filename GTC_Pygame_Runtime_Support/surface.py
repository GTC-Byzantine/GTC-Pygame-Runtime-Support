import pygame

class CommonSurface:
    def __init__(self, size, pos, screen):
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface(size)
        self.screen = screen
        self.checkers = []
    def add_checker(self, checker, motion):
        
