import pygame
from typing import Tuple, List, Callable
from .basic_class import BasicButton
from .button_support import FeedbackButton


class BasicPage:

    def __init__(self, width, height, pos, screen = None):
        """

        :param width:           宽度
        :type width:            int
        :param height:          高度
        :type height:           int
        :param pos:             在目标 Surface 的位置
        :type pos:              (int, int) | List[int, int]
        :param screen:          目标 Surface 对象
        :type screen:           pygame.Surface | pygame.surface.SurfaceType | None

        """
        self.size = [width, height]
        self.surface = pygame.Surface(self.size)
        self.pos = pos
        self.screen = screen
        self.sliding = False
        self.button_trusteeship: Callable[[List[BasicButton], List[FeedbackButton]], None] = [FeedbackButton]

BasicPage