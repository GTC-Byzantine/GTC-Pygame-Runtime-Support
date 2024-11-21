import sys
from typing import Tuple, List
import pygame

pygame.font.init()
pygame.display.init()

#####
class ProgressBar:
    process = 0

    def __init__(self, width: int, height: int, target: pygame.Surface, pos: List[int],
                 color: Tuple[Tuple[int, int, int], Tuple[int, int, int]] = ([0, 0, 0], [0, 255, 0]), sep: int = 5,
                 border=None):
        self.surface = pygame.Surface((width, height))
        self.background_color = color[0]
        self.bar_color = color[1]
        self.sep = sep
        self.height = height
        self.width = width
        self.screen = target
        self.pos = pos
        self.border = border

    def next(self):
        self.process += self.sep
        self.surface.fill(self.background_color)
        if self.border is not None:
            pygame.draw.rect(self.surface, self.border, (0, 0, self.width, self.height), width=1)
        pygame.draw.rect(self.surface, self.bar_color, (0, 0, self.process, self.height))
        self.screen.blit(self.surface, self.pos)
#####

if __name__ == '__main__':
    screen = pygame.display.set_mode((500, 500))
    pb = ProgressBar(400, 10, screen, [50, 250], border=[255, 255, 255])
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pb.next()
        pygame.display.update()
        clock.tick(60)

# From GTC Pygame Runtime Support.
# Copyright © 2024 GTC Software Studio . All Rights Reserved.
