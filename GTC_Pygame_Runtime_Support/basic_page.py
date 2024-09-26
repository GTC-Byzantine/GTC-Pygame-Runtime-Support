import pygame
from typing import List
from basic_class import *


class BasicPage:

    def __init__(self, width, height, pos, screen=None):
        """

        :param width:           宽度
        :type width:            int
        :param height:          高度
        :type height:           int
        :param pos:             在目标 Surface 的位置
        :type pos:              Tuple[int, int] | List[int, int]
        :param screen:          目标 Surface 对象
        :type screen:           pygame.Surface | pygame.surface.SurfaceType | None

        """
        self.size = [width, height]
        self.frame = pygame.Surface(self.size)
        self.surface = pygame.Surface(self.size)
        self.pos = pos
        self.screen = screen
        self.sliding = False
        self.button_trusteeship: List[BasicButton] = []
        self.delta = 0
        self.pos_y = 0
        self.pre_click = False
        self.pre_pos: List[int] = [0, 0]

    def operate(self, mouse_pos, effectiveness):
        """
        :param mouse_pos:
        :type mouse_pos:            List[int, int] | (int, int)
        :param effectiveness:
        :type effectiveness:        bool
        :return:                    None
        """

        if not self.pre_click and effectiveness:
            self.pre_pos = mouse_pos
            
            self.sliding = False

        elif self.pre_click and effectiveness:
            if self.pre_pos != mouse_pos:
                self.sliding = True
            self.delta = mouse_pos[1] - self.pre_pos[1]

        elif self.pre_click and not effectiveness:
            self.sliding = False
            self.pos_y += self.delta
            self.delta = 0

        self.frame.fill((0, 0, 0))
        self.frame.blit(self.surface, (0, self.pos_y + self.delta))
        if self.screen is not None:
            self.screen.blit(self.frame, self.pos)

        self.pre_click = effectiveness
        print(self.pos_y, self.sliding)
