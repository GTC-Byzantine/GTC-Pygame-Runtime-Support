import pygame
from typing import List
from basic_class import *


class BasicPage:

    def __init__(self, show_size, real_size, pos, screen=None, acc=1):
        """

        :param show_size:
        :type show_size:            Tuple[int, int] | List[int, int]
        :param real_size:
        :type real_size:           Tuple[int, int] | List[int, int]
        :param pos:             在目标 Surface 的位置
        :type pos:              Tuple[int, int] | List[int, int]
        :param screen:          目标 Surface 对象
        :type screen:           pygame.Surface | pygame.surface.SurfaceType | None
        :param acc:
        :type acc:              float
        """
        self.size = show_size
        self.real_size = real_size
        self.frame = pygame.Surface(self.size)
        self.surface = pygame.Surface(self.real_size)
        self.pos = pos
        self.screen = screen
        self.sliding = False
        self.button_trusteeship: List[BasicButton] = []
        self.delta = 0
        self.pos_y = 0
        self.pre_click = False
        self.pre_pos: List[int] = [0, 0]
        self.acc = acc
        self.speed = 0
        self.last_delta = 0
        self.ps = 0
        self.lock = False

    def _in_area(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    def _reverse(self):
        if self.pos_y > 0:
            self.pos_y /= self.acc
            self.speed = 0
        elif self.pos_y < self.size[1] - self.real_size[1]:
            self.pos_y = (self.pos_y + self.real_size[1] - self.size[1]) / self.acc + self.size[1] - self.real_size[1]

    def operate(self, mouse_pos, effectiveness):
        """
        :param mouse_pos:
        :type mouse_pos:            List[int, int] | (int, int)
        :param effectiveness:
        :type effectiveness:        bool
        :return:                    None
        """
        if self._in_area(mouse_pos) or self.sliding:
            if not self.lock:
                if not self.pre_click and effectiveness:
                    self.pre_pos = mouse_pos
                    self.ps = 1
                    self.sliding = False
                    self.lock = False

                elif self.pre_click and effectiveness:
                    if self.pre_pos != mouse_pos:
                        self.sliding = True
                    self.delta = mouse_pos[1] - self.pre_pos[1]
                    self.speed = self.delta - self.last_delta
                    self.last_delta = self.delta
                    self.ps += 1

                elif self.pre_click and not effectiveness:
                    self.sliding = False
                    self.pos_y += self.delta
                    print(self.speed)
                    self.delta = 0

                else:
                    self._reverse()
                    self.pos_y += self.speed
                    self.speed /= self.acc
        else:
            self._reverse()
            self.pos_y += self.speed
            self.speed /= self.acc
            if effectiveness:
                self.lock = True
            else:
                self.lock = False
        self.frame.fill((0, 0, 0))
        self.frame.blit(self.surface, (0, self.pos_y + self.delta))
        if self.screen is not None:
            self.screen.blit(self.frame, self.pos)

        self.pre_click = effectiveness
        # print(self.pos_y, self.sliding)
