import pygame
from typing import List
from GTC_Pygame_Runtime_Support.basic_class import *
from GTC_Pygame_Runtime_Support.error import *


#####
class PlainPage:

    def __init__(self, show_size, real_size, pos, screen=None, acc=1.4, wheel_support=False, grounding=(220, 220, 220)):
        """

        :param show_size:           显示的大小
        :type show_size:            Tuple[int, int] | List[int]
        :param real_size:           实际的大小
        :type real_size:            Tuple[int, int] | List[int]
        :param pos:                 在目标 Surface 的位置
        :type pos:                  Tuple[int, int] | List[int]
        :param screen:              目标 Surface 对象
        :type screen:               pygame.Surface | pygame.surface.SurfaceType | None
        :param acc:                 动画加速度
        :type acc:                  float
        :param wheel_support:       是否支持滚轮
        :type wheel_support:        bool
        :param grounding:           虚空部分底色
        :type grounding:            (int, int, int) | List[int]
        """
        self._size = show_size
        self._real_size = real_size
        self._frame = pygame.Surface(self._size)
        self.surface = pygame.Surface(self._real_size)
        self._pos = pos
        self._screen = screen
        self._sliding = False
        self._button_trusteeship: List[BasicButton] = []
        self._delta = 0
        self._pos_y = 0
        self._pre_click = False
        self._pre_pos: List[int] = [0, 0]
        self._acc = acc
        self._speed = 0
        self._last_delta = 0
        self._ps = 0
        self._lock = False
        self._wheel_support = wheel_support
        self._background = None
        self._grounding = grounding

    def add_button_trusteeship(self, button):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__class__.__name__))
        self._button_trusteeship.append(button)

    def set_as_background(self):
        self._background = self.surface.copy()

    def change_blit_pos(self, pos):
        """
        :param pos:         更改后的坐标
        :type pos:          (int, int) | List[int]
        :return:
        """
        self._pos = pos

    def _in_area(self, mouse_pos):
        if self._pos[0] <= mouse_pos[0] <= self._size[0] + self._pos[0] and self._pos[1] <= mouse_pos[1] <= self._size[
            1] + self._pos[1]:
            return True
        return False

    def _reverse(self):
        if self._pos_y > 0:
            self._pos_y /= self._acc
        elif self._pos_y < self._size[1] - self._real_size[1]:
            self._pos_y = (self._pos_y + self._real_size[1] - self._size[1]) / self._acc + self._size[1] - \
                          self._real_size[1]

    def operate(self, mouse_pos, effectiveness, mouse_wheel_status=None, operate_buttons=False):
        """
        :param mouse_pos:
        :type mouse_pos:            List[int] | (int, int)
        :param effectiveness:
        :type effectiveness:        bool
        :param mouse_wheel_status:
        :type mouse_wheel_status:   [bool, bool] | None
        :param operate_buttons:
        :type operate_buttons:      False
        :return:                    None

        """
        if self._background is not None:
            self.surface.blit(self._background, (0, 0))
            # pass
        if self._in_area(mouse_pos) and self._wheel_support and not effectiveness:
            if mouse_wheel_status is None:
                raise UnexpectedParameter(error0x01)
            if mouse_wheel_status[0]:
                self._speed = -20
            elif mouse_wheel_status[1]:
                self._speed = 20
        if self._in_area(mouse_pos) or self._sliding:
            if not self._lock:
                if not self._pre_click and effectiveness:
                    self._pre_pos = mouse_pos
                    self._ps = 1
                    self._sliding = False
                    self._lock = False

                elif self._pre_click and effectiveness:
                    if self._pre_pos != mouse_pos:
                        self._sliding = True
                    self._delta = mouse_pos[1] - self._pre_pos[1]
                    self._speed = self._delta - self._last_delta
                    self._last_delta = self._delta
                    self._ps += 1

                elif self._pre_click and not effectiveness:
                    self._sliding = False
                    self._pos_y += self._delta
                    self._delta = 0

                else:
                    self._reverse()
                    self._pos_y += self._speed
                    self._speed /= self._acc
            else:
                if not effectiveness:
                    self._lock = False
        else:
            self._reverse()
            self._pos_y += self._speed
            self._speed /= self._acc
            if effectiveness:
                self._lock = True
            else:
                self._lock = False
        if operate_buttons:
            for item in self._button_trusteeship:
                item.operate((mouse_pos[0] - self._pos[0], mouse_pos[1] - self._pos[1] - self._pos_y), effectiveness)
                if self._sliding:
                    item.cancel()
        self._frame.fill(self._grounding)
        self._frame.blit(self.surface, (0, self._pos_y + self._delta))
        if self._screen is not None:
            self._screen.blit(self._frame, self._pos)

        self._pre_click = effectiveness
        # print(self.pos_y, self.sliding)

#####
