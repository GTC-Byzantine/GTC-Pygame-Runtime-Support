import pygame
import os
from typing import Tuple, List


class BasicButton(object):
    state = False

    def __init__(self):
        self.do_cancel = False

    def operate(self, mouse_pos, effectiveness):
        """

        :param mouse_pos:
        :type mouse_pos:            (int, int) | List[int, int]
        :param effectiveness:
        :type effectiveness:        bool
        :return:
        """
        self.do_cancel: bool = False

    def cancel(self):
        self.state = False
        self.do_cancel = True


error0x01 = '滚轮支持开启后，mouse_wheel_status 应为(bool, bool)而非 None'
error0x02 = '参数应为 {} 的实例'


class UnexpectedParameter(Exception):
    def __init__(self, info):
        super().__init__()
        self.info = info

    def __str__(self):
        return self.info


class BasicPage:

    def __init__(self, show_size, real_size, pos, screen=None, acc=1, wheel_support=False):
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

    def add_button_trusteeship(self, button):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__class__.__name__))
        self._button_trusteeship.append(button)

    def set_as_background(self):
        self._background = self.surface.copy()

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
        if self._in_area(mouse_pos) and self._wheel_support:
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
            self._reverse()
            self._pos_y += self._speed
            self._speed /= self._acc
            if effectiveness:
                self._lock = True
            else:
                self._lock = False
        if operate_buttons:
            for item in self._button_trusteeship:
                item.operate((mouse_pos[0] - self._pos[0], mouse_pos[1] - self._pos[1] + self._pos_y), effectiveness)

        self._frame.fill((0, 0, 0))
        self._frame.blit(self.surface, (0, self._pos_y + self._delta))
        if self._screen is not None:
            self._screen.blit(self._frame, self._pos)

        self._pre_click = effectiveness
        # print(self.pos_y, self.sliding)


class FeedbackButton(BasicButton):
    # 初始化反馈按钮
    def __init__(self, size, pos, text, text_size, surface, bg_color=(30, 255, 189), border_color=(255, 255, 255),
                 change_color=((0, 112, 255), (0, 255, 112)), text_color=(0, 0, 0), speed=2, font_type='SimHei'):
        """
        :param size:            按钮大小
        :type size:             List[int, int] | (int, int)
        :param pos:             按钮在目标 Surface 上的位置
        :type pos:              List[int, int] | (int, int)
        :param text:            按钮的显示文本
        :type text:             str
        :param text_size:       文本字体大小
        :type text_size:        int
        :param surface:         目标 Surface
        :type surface:          pygame.surface.SurfaceType | pygame.surface.Surface
        :param bg_color:        按钮背景颜色
        :type bg_color:         (int, int, int) | List[int, int, int]
        :param border_color:    按钮边框颜色
        :type border_color:     (int, int, int) | List[int, int, int]
        :param change_color:    按钮点击时的颜色变化
        :type change_color:     ((int, int, int), (int, int, int))
        :param text_color:      文字颜色
        :type text_color:       (int, int, int) | List[int, int, int]
        :param speed:           变化速度
        :type speed:            int
        :param font_type:       字体样式（名称或路径）
        :type font_type:        str
        """
        super().__init__()
        self.size = size
        self.pos = pos

        if os.path.exists(font_type):
            self.text = pygame.font.Font(font_type, text_size).render(text, True, text_color)
        else:
            self.text = pygame.font.SysFont(font_type, text_size).render(text, True, text_color)
        self.color = [bg_color, border_color, change_color]
        self.font_rect = self.text.get_rect()

        self.font_rect.center = (pos[0] + size[0] // 2, pos[1] + size[1] // 2)
        self.iter = 0
        self.color_iter = 0
        self.speed = speed

        self.color_delta = [(self.color[2][0][0] - self.color[2][1][0]) / 4,
                            (self.color[2][0][1] - self.color[2][1][1]) / 4,
                            (self.color[2][0][2] - self.color[2][1][2]) / 4]
        self.surface = surface
        self.temp_color = [0, 0, 0]
        self.state = False
        self.lock = False
        self.last_clicked = False

    def in_area(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    def operate(self, mouse_pos, effectiveness):
        if self.in_area(mouse_pos):
            self.iter += self.speed
            self.iter = min(self.iter, 12)
            if effectiveness and not self.lock:
                if not self.last_clicked:
                    self.do_cancel = False
                    self.last_clicked = True
                self.color_iter += 1
                self.color_iter = min(4, self.color_iter)
                self.state = True
            else:
                self.color_iter -= 1
                self.color_iter = max(0, self.color_iter)
                self.state = False
            if self.lock and not effectiveness:
                self.lock = False
        else:
            self.iter -= self.speed
            self.iter = max(0, self.iter)
            self.color_iter -= 1
            self.color_iter = max(0, self.color_iter)
            self.state = False
            if effectiveness:
                self.lock = True
            else:
                self.lock = False
        if not self.state:
            self.last_clicked = False
        self.temp_color = list(self.color[2][0])

        for item in range(len(self.temp_color)):
            self.temp_color[item] -= self.color_iter * self.color_delta[item]

        pygame.draw.rect(self.surface, self.temp_color, (self.pos[0] - self.iter, self.pos[1] - self.iter,
                                                         self.size[0] + 2 * self.iter, self.size[1] + 2 * self.iter),
                         border_radius=min(self.size) // 4, width=6)
        pygame.draw.rect(self.surface, self.color[0], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4)
        pygame.draw.rect(self.surface, self.color[1], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4, width=4)

        self.surface.blit(self.text, self.font_rect)

    def change_pos(self, pos: Tuple[int, int]):
        self.pos = pos
        self.font_rect.center = (pos[0] + self.size[0] // 2, pos[1] + self.size[1] // 2)


class DelayButton(BasicButton):
    # 初始化延迟响应按钮
    def __init__(self, size, pos, text, text_size, surface, bg_color=(30, 255, 189), border_color=(255, 255, 255),
                 change_color=((0, 112, 255), (0, 255, 112)), text_color=(0, 0, 0), speed=2, font_type='SimHei'):
        """
        :param size:            按钮大小
        :type size:             List[int, int] | (int, int)
        :param pos:             按钮在目标 Surface 上的位置
        :type pos:              List[int, int] | (int, int)
        :param text:            按钮的显示文本
        :type text:             str
        :param text_size:       文本字体大小
        :type text_size:        int
        :param surface:         目标 Surface
        :type surface:          pygame.surface.SurfaceType | pygame.surface.Surface
        :param bg_color:        按钮背景颜色
        :type bg_color:         (int, int, int) | List[int, int, int]
        :param border_color:    按钮边框颜色
        :type border_color:     (int, int, int) | List[int, int, int]
        :param change_color:    按钮点击时的颜色变化
        :type change_color:     ((int, int, int), (int, int, int))
        :param text_color:      文字颜色
        :type text_color:       (int, int, int) | List[int, int, int]
        :param speed:           变化速度
        :type speed:            int
        :param font_type:       字体样式（名称或路径）
        :type font_type:        str
        """
        super().__init__()
        self.size = size
        self.pos = pos

        if os.path.exists(font_type):
            self.text = pygame.font.Font(font_type, text_size).render(text, True, text_color)
        else:
            self.text = pygame.font.SysFont(font_type, text_size).render(text, True, text_color)
        self.color = [bg_color, border_color, change_color]
        self.font_rect = self.text.get_rect()
        self.font_rect.center = (pos[0] + size[0] // 2,
                                 pos[1] + size[1] // 2)
        self.iter = 0
        self.color_iter = 0
        self.speed = speed
        self.color_delta = [(self.color[2][0][0] - self.color[2][1][0]) / 4,
                            (self.color[2][0][1] - self.color[2][1][1]) / 4,
                            (self.color[2][0][2] - self.color[2][1][2]) / 4]
        self.surface = surface
        self.temp_color = [0, 0, 0]
        self.state_1 = False
        self.state_2 = False
        self.last = False
        self.click = 0
        self.last_clicked = False

    def in_area(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    def operate(self, mouse_pos, effectiveness):
        if self.in_area(mouse_pos):
            self.state_2 = True
            if effectiveness:
                self.state_1 = True
                if not self.last_clicked:
                    self.do_cancel = False
                    self.last_clicked = True
                if not self.last:
                    self.last = True
                    self.click += 1
            else:
                self.last = False
        else:
            if effectiveness:
                self.state_2 = False
                self.state_1 = False
                self.last = False
                self.click = 0
            if not self.state_1:
                self.state_2 = False
        if not self.state:
            self.last_clicked = False
        if self.state_2:
            self.iter += self.speed
            self.iter = min(self.iter, 12)
        else:
            self.iter -= self.speed
            self.iter = max(self.iter, 0)
        if self.state_1:
            self.color_iter += 1
            self.color_iter = min(4, self.color_iter)
        else:
            self.color_iter -= 1
            self.color_iter = max(0, self.color_iter)

        self.temp_color = list(self.color[2][0])

        for item in range(len(self.temp_color)):
            self.temp_color[item] -= self.color_iter * self.color_delta[item]

        pygame.draw.rect(self.surface, self.temp_color, (self.pos[0] - self.iter, self.pos[1] - self.iter,
                                                         self.size[0] + 2 * self.iter, self.size[1] + 2 * self.iter),
                         border_radius=min(self.size) // 4, width=6)
        pygame.draw.rect(self.surface, self.color[0], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4)
        pygame.draw.rect(self.surface, self.color[1], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4, width=4)

        self.surface.blit(self.text, self.font_rect)


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


class Slider:

    def __init__(self, background: pygame.Surface, acceleration: float, surface: pygame.Surface,
                 direction: tuple[int, int] = (1, 0), initial_speed: int = 5, previous_image=None,
                 slide_with=False, screen_background=None):
        self.size = surface.get_size()
        self.image = pygame.transform.scale(background, self.size)
        self.acceleration = acceleration
        self.speed: float = 0
        self.surface = surface
        if not isinstance(direction, tuple) or direction[0] not in [-1, 0, 1] or direction[1] not in [-1, 0, 1]:
            raise TypeError('666 不看文档嘛')
        self.start_pos = [direction[0] * self.size[0], direction[1] * self.size[1]]
        self.speed_vector = [-direction[0], -direction[1]]
        self.initial_speed = initial_speed
        self.speed = [0, 0]
        self.acceleration = acceleration
        self.pos = self.start_pos.copy()
        self.image_status = previous_image
        self.do_slide = slide_with
        self.background = pygame.transform.scale(screen_background, self.size)
        if isinstance(self.image_status, pygame.Surface):
            self.image_status = pygame.transform.scale(self.image_status, self.size)

    def next_frame(self):

        if abs(self.pos[0] + self.speed[0]) <= 10 and abs(self.pos[1] + self.speed[1]) <= 10:
            return True
        else:
            self.surface.fill((255, 255, 255))
            if self.background is not None:
                self.surface.blit(self.background, (0, 0))
            if self.image_status is not None:
                if self.do_slide:
                    self.surface.blit(self.image_status, (self.pos[0] - self.size[0], self.pos[1] - self.size[1]))
                else:
                    self.surface.blit(self.image_status, (0, 0))
            for i in [0, 1]:
                self.speed[i] += self.speed_vector[i] * self.acceleration
                self.pos[i] += self.speed[i]
            self.surface.blit(self.image, self.pos)
            print(self.pos)
            pygame.display.flip()
        return False
