import os
from typing import *
from typing import List, Tuple
import pygame
from GTC_Pygame_Runtime_Support.basic_class import *
from GTC_Pygame_Runtime_Support.supported_types import *

pygame.font.init()
pygame.display.init()


class FeedbackButton(BasicButton):
    def __init__(self, size, pos, text, text_size, surface, bg_color=(30, 255, 189), border_color=(255, 255, 255),
                 change_color=((0, 112, 255), (0, 255, 112)), text_color=(0, 0, 0), speed=2, font_type='SimHei'):
        """
        :param size:            按钮大小
        :type size:             List[int] | (int, int)
        :param pos:             按钮在目标 Surface 上的位置
        :type pos:              List[int] | (int, int)
        :param text:            按钮的显示文本
        :type text:             str
        :param text_size:       文本字体大小
        :type text_size:        int
        :param surface:         目标 Surface
        :type surface:          pygame.surface.SurfaceType | pygame.surface.Surface
        :param bg_color:        按钮背景颜色
        :type bg_color:         (int, int, int) | List[int]
        :param border_color:    按钮边框颜色
        :type border_color:     (int, int, int) | List[int]
        :param change_color:    按钮点击时的颜色变化
        :type change_color:     ((int, int, int), (int, int, int))
        :param text_color:      文字颜色
        :type text_color:       (int, int, int) | List[int]
        :param speed:           变化速度
        :type speed:            int
        :param font_type:       字体样式（名称或路径）
        :type font_type:        str
        """
        super().__init__()
        self.size = size
        self.pos = pos
        self.frame = pygame.Surface(size).convert_alpha()
        if os.path.exists(font_type):
            self.text = pygame.font.Font(font_type, text_size).render(text, True, text_color)
        else:
            self.text = pygame.font.SysFont(font_type, text_size).render(text, True, text_color)
        self.color = [bg_color, border_color, change_color]
        self.font_rect = self.text.get_rect()

        self.font_rect.center = (size[0] // 2, size[1] // 2)
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
        self.on_click = False

    def in_area(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + self.pos[1]:
            return True
        return False

    def operate(self, mouse_pos, mouse_press):
        """
        :param mouse_pos:           鼠标坐标
        :type mouse_pos:            List[int] | Tuple[int, int]
        :param mouse_press:         鼠标状态
        :type mouse_press:          List[bool] | Tuple[bool, bool, bool] | Tuple[bool, bool, bool, bool, bool]
        :return:
        """
        self.frame.fill((0, 0, 0, 0))
        if self.in_area(mouse_pos):
            self.iter += self.speed
            self.iter = min(self.iter, 12)
            if mouse_press[0] and not self.lock:
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
            if self.lock and not mouse_press[0]:
                self.lock = False
        else:
            self.iter -= self.speed
            self.iter = max(0, self.iter)
            self.color_iter -= 1
            self.color_iter = max(0, self.color_iter)
            self.state = False
            if mouse_press[0]:
                self.lock = True
                if self.last_clicked:
                    self.cancel()
            else:
                self.lock = False
        if not mouse_press[0] and self.last_clicked and not self.do_cancel:
            self.on_click = True
        else:
            self.on_click = False
        if not self.state:
            self.last_clicked = False
        self.temp_color = list(self.color[2][0])

        for item in range(len(self.temp_color)):
            self.temp_color[item] -= self.color_iter * self.color_delta[item]

        pygame.draw.rect(self.surface, self.temp_color, (self.pos[0] - self.iter, self.pos[1] - self.iter,
                                                         self.size[0] + 2 * self.iter, self.size[1] + 2 * self.iter),
                         border_radius=min(self.size) // 4, width=6)
        pygame.draw.rect(self.frame, self.color[0], [0, 0, self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4)
        pygame.draw.rect(self.frame, self.color[1], [0, 0, self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4, width=4)

        self.frame.blit(self.text, self.font_rect)
        self.surface.blit(self.frame, self.pos)

    def change_pos(self, pos: Tuple[int, int]):
        self.pos = pos


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
        :type bg_color:         (int, int, int) | List[int]
        :param border_color:    按钮边框颜色
        :type border_color:     (int, int, int) | List[int]
        :param change_color:    按钮点击时的颜色变化
        :type change_color:     ((int, int, int), (int, int, int))
        :param text_color:      文字颜色
        :type text_color:       (int, int, int) | List[int]
        :param speed:           变化速度
        :type speed:            int
        :param font_type:       字体样式（名称或路径）
        :type font_type:        str
        """
        super().__init__()
        self.size = size
        self.pos = pos
        self.frame = pygame.Surface(size).convert_alpha()
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

    def operate(self, mouse_pos, mouse_press):
        """
        :param mouse_pos:           鼠标坐标
        :type mouse_pos:            List[int] | Tuple[int, int]
        :param mouse_press:         鼠标状态
        :type mouse_press:          List[bool] | Tuple[bool, bool, bool] | Tuple[bool, bool, bool, bool, bool]
        :return:
        """
        self.frame.fill((0, 0, 0, 0))
        if self.in_area(mouse_pos):
            self.state_2 = True
            if mouse_press[0]:
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
            if mouse_press[0]:
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
        pygame.draw.rect(self.frame, self.color[0], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4)
        pygame.draw.rect(self.frame, self.color[1], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4, width=4)

        self.frame.blit(self.text, self.font_rect)
        self.surface.blit(self.frame, self.pos)

    def change_pos(self, pos: Tuple[int, int]):
        self.pos = pos


class SimpleButtonWithImage(BasicButton):
    def __init__(self, pos: Coordinate, surface: pygame.Surface, size: Coordinate = (200, 200),
                 bg_color: ColorValue = (255, 255, 255),
                 hovering_color: ColorValue = (249, 249, 249),
                 clicking_color: ColorValue = (252, 248, 245),
                 bg_image: pygame.Surface or None = None,
                 text: Union[Tuple[str, Coordinate, int, ColorValue]] = ('', (0, 0), 1, (0, 0, 0)),
                 font: str = 'SimHei', border_radius: int=10, border_width: int = 2):
        super().__init__()
        self.size = size
        self.bg_color = bg_color
        self.hovering = hovering_color
        self.clicking = clicking_color
        self.pos = pos
        self.bg_image = None
        if bg_image is not None:
            self.bg_image = pygame.transform.scale(bg_image, size)
        self.surface = surface
        self.lock = False
        self.state = False
        self.text_ini = text
        self.text_size = None
        self.text_color = None
        self.text_pos = [text[1][0] + pos[0], text[1][1] + pos[1]]
        self.cp = []
        self.last_clicked = False
        self.on_click = False
        self.border_radius = border_radius
        self.border_width = border_width
        if text is not None:
            self.text_size = text[2]
            self.text_color = text[3]
            if os.path.exists(font):
                self.text = pygame.font.Font(font, self.text_size).render(text[0], True, self.text_color)
            else:
                self.text = pygame.font.SysFont(font, self.text_size).render(text[0], True, self.text_color)

    def _in_area(self, mouse_pos: Tuple[int, int] or List[int]):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    def operate(self, mouse_pos, mouse_press):
        """
        :param mouse_pos:           鼠标坐标
        :type mouse_pos:            List[int] | Tuple[int, int]
        :param mouse_press:         鼠标状态
        :type mouse_press:          List[bool] | Tuple[bool, bool, bool] | Tuple[bool, bool, bool, bool, bool]
        :return:
        """
        if self._in_area(mouse_pos):
            if mouse_press[0] and not self.lock:
                self.state = True
                if not self.last_clicked:
                    self.do_cancel = False
                    self.last_clicked = True
                pygame.draw.rect(self.surface, self.clicking, [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                                 border_radius=self.border_radius)
            else:
                self.state = False
                pygame.draw.rect(self.surface, self.hovering, [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                                 border_radius=self.border_radius)
            if self.lock and not mouse_press[0]:
                self.lock = False

        else:
            pygame.draw.rect(self.surface, self.bg_color, [self.pos[0], self.pos[1], self.size[0], self.size[1]], border_radius=self.border_radius)
            if mouse_press[0]:
                self.lock = True
                if self.last_clicked:
                    self.cancel()
            else:
                self.lock = False
        if not mouse_press[0] and self.last_clicked and not self.do_cancel:
            self.on_click = True
        else:
            self.on_click = False
        if not self.state:
            self.last_clicked = False
        if self.bg_image is not None:
            self.surface.blit(self.bg_image, self.pos)
        if self.border_width:
            pygame.draw.rect(self.surface, (0, 0, 0), [self.pos[0], self.pos[1], self.size[0], self.size[1]], width=self.border_width, border_radius=self.border_radius)

        if self.text_ini is not None:
            self.surface.blit(self.text, self.text.get_rect(center=self.text_pos))

    def change_pos(self, pos: Tuple[int, int]):
        self.pos = pos
