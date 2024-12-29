import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicPopup


class SimplePopup(BasicPopup):
    def show(self):
        self.screen.blit(self.surface, self.pos)

    def loop(self, function, args):
        function(*args)

