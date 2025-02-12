import pygame
from typing import List
import ctypes
from ctypes import wintypes


class DragArea:
    rect_list: List[pygame.Rect] = []
    last_clicked = False
    origin_pos = [-1, -1]
    lock = False
    operating = False
    user32 = ctypes.windll.user32

    def __init__(self, hwnd, s_width, s_height):
        """
        :param hwnd:                窗口的hwnd值
        :type hwnd:                 int
        :param s_width:             屏幕宽度
        :type s_width:              int
        :param s_height:            屏幕高度
        :type s_height:             int
        """
        self.hwnd = hwnd
        rect = ctypes.wintypes.RECT()
        self.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        self.now_pos = list((rect.left, rect.top))
        self.screen_size = [s_width, s_height]

    def in_area(self, mouse_pos):
        """
        :param mouse_pos:       鼠标位置
        :type mouse_pos:        List[int] | Tuple[int, int]
        :return:
        """
        for rect in self.rect_list:
            if rect.collidepoint(*mouse_pos):
                return True
        return False

    def add_rect(self, rect: pygame.Rect):
        self.rect_list.append(rect)

    def modify(self, mouse_pos, mouse_press):
        """
        :param mouse_pos:           鼠标坐标
        :type mouse_pos:            List[int] | Tuple[int, int]
        :param mouse_press:         鼠标状态
        :type mouse_press:          List[bool] | Tuple[bool, bool, bool] | Tuple[bool, bool, bool, bool, bool]
        :return:
        """
        if mouse_press[0] and not self.in_area(mouse_pos) and not self.operating:
            self.lock = True

        if mouse_press[0] and ((self.in_area(mouse_pos) and not self.lock) or self.operating):
            if not self.operating:
                self.origin_pos = list(mouse_pos)
                self.operating = True
            else:
                delta_x = mouse_pos[0] - self.origin_pos[0]
                delta_y = mouse_pos[1] - self.origin_pos[1]
                self.now_pos[0] += delta_x
                self.now_pos[1] += delta_y
                self.user32.MoveWindow(self.hwnd, self.now_pos[0], self.now_pos[1], self.screen_size[0], self.screen_size[1], True)

        if not mouse_press[0]:
            self.operating = False
            self.lock = False


if __name__ == '__main__':
    screen = pygame.display.set_mode((800, 600), flags=pygame.NOFRAME)
    # pygame.init()
    da = DragArea(pygame.display.get_wm_info()['window'], screen.get_width(), screen.get_height())
    da.add_rect(pygame.Rect(0, 0, 800, 600))
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        da.modify(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        clock.tick(60)
