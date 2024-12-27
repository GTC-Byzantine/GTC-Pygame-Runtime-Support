import sys
from typing import Tuple, List
import pygame

pygame.font.init()
pygame.display.init()


class ProgressBar:
    progress = 0
    def __init__(self, width, height, target: pygame.Surface, pos, color = ((0, 0, 0), (0, 255, 0)), sep = 5, border=None):
        """
        :param width:                       进度条宽度
        :type width:                        int
        :param height:                      进度条高度
        :type height:                       int
        :param target:                      要在哪个 Surface 上呈现
        :type target:                       pygame.SurfaceType
        :param pos:                         在目标 Surface 的位置
        :type pos:                          List[int] | Tuple[int, int]
        :param color:                       进度条背景色及前景色
        :type color:                        Tuple[Tuple[int, int, int], Tuple[int, int, int]] | Tuple[List[int], List[int]]
        :param sep:                         每次操作前进的步长
        :type sep:                          int
        :param border:                      边框颜色（可以为空）
        :type border:                       None
        """
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
        self.progress += self.sep
        self.surface.fill(self.background_color)
        if self.border is not None:
            pygame.draw.rect(self.surface, self.border, (0, 0, self.width, self.height), width=1)
        pygame.draw.rect(self.surface, self.bar_color, (0, 0, self.progress, self.height))
        self.screen.blit(self.surface, self.pos)


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
