import sys
import pygame
import os
from typing import List, Tuple
from GTC_Pygame_Runtime_Support.basic_class import *

pygame.init()


#####

class FeedbackButton(BasicButton):
    # 初始化反馈按钮
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
        self.on_click = False

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
                if self.last_clicked:
                    self.cancel()
            else:
                self.lock = False
        if not effectiveness and self.last_clicked and not self.do_cancel:
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


#####

if __name__ == '__main__':
    s = pygame.display.set_mode((500, 500))
    b = FeedbackButton([280, 80], (100, 100), '课堂小记', 62, s,
                       bg_color=[0, 145, 220],
                       border_color=[209, 240, 255], text_color=(255, 255, 255),
                       change_color=((0, 145, 220), (0, 220, 145)))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(998244353)
        s.fill((0, 0, 0))
        b.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if b.on_click:
            print(1)
        pygame.display.flip()
        clock.tick(60)

