import os
from typing import List

import pygame
from pygame import SurfaceType

from GTC_Pygame_Runtime_Support.error import UnexpectedParameter, error0x02

pygame.display.init()


class BasicButton(object):
    state = False

    def __init__(self):
        self.do_cancel = False
        self.cp = []

    def operate(self, mouse_pos, effectiveness):
        """
        :param mouse_pos:
        :type mouse_pos:            (int, int) | List[int]
        :param effectiveness:
        :type effectiveness:        bool
        :return:
        """
        self.do_cancel: bool = False

    def cancel(self):
        self.state = False
        self.do_cancel = True


class BasicChecker(object):
    def __init__(self, check_range, default_state=False, do_reverse=False):
        """
        :param check_range:             检查的范围（横纵长宽）
        :type check_range:              List[int] | Tuple[int, int, int, int]
        :param default_state:           默认状态
        :type default_state:            bool | int | str
        """
        self.range = check_range
        self._state = default_state
        self._do_reverse = do_reverse
        self.cp = []

    def check(self, mouse_pos, mouse_click):
        """
        :param mouse_pos:
        :type mouse_pos:                        (int, int) | List[int]
        :param mouse_click:
        :type mouse_click:                      (bool, bool, bool, bool, bool) | List[int]
        :return:                                bool
        """
        pass

    def change_range(self, check_range):
        self.range = check_range

    def add_pos(self, pos):
        self.range[0] = pos[0]
        self.range[1] = pos[1]


class BasicSurface:
    def __init__(self, size, pos, screen):
        self._size = size
        self._pos = pos
        self.surface: SurfaceType = pygame.Surface(size).convert_alpha()
        self._screen: SurfaceType = screen
        self._checkers = {}
        self._button_trusteeship: List[BasicButton] = []
        self.do_element_show = []
        self._background = None
        self.cp = []

    def set_as_background(self):
        self._background = self.surface.copy()

    def add_button_trusteeship(self, button: BasicButton):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__name__))
        self._button_trusteeship.append(button)
        self.do_element_show.append(False)

    def show_button_trusteeship(self):
        return self._button_trusteeship

    def operate_button(self, mouse_pos, effectiveness, do_cancel):
        for button in self._button_trusteeship:
            if self.do_element_show[self._button_trusteeship.index(button)]:
                button.operate(mouse_pos, effectiveness)
                if do_cancel:
                    button.cancel()

    def operate(self, mouse_pos, effectiveness, do_cancel=False):
        if self._background is not None:
            self.surface.blit(self._background, (0, 0))
        else:
            self.surface.fill((0, 0, 0, 0))
        self.operate_button([mouse_pos[0] - self._pos[0], mouse_pos[1] - self._pos[1]], effectiveness, do_cancel)
        self._screen.blit(self.surface, self._pos)

    def run_check(self, mouse_pos, mouse_click) -> bool:
        """
        :param mouse_pos:
        :type mouse_pos:                        (int, int) | List[int]
        :param mouse_click:
        :type mouse_click:                      (bool, bool, bool, bool, bool) | List[int]
        :return:
        """
        pass

    def add_checker_group(self, group_name, motion, args, checker_type='and'):
        """
        :param args:
        :type args:                     List[]
        :param group_name:
        :type group_name:               str
        :param motion:
        :type motion:                   function
        :param checker_type:
        :type checker_type:             str
        :return:                        None
        """
        self._checkers[group_name] = {'checkers': [], 'motion': motion, 'args': args, 'type': checker_type}

    def add_checker(self, group_name, checker, is_relative=False):
        """
        :param is_relative:
        :type is_relative:              bool
        :param checker:
        :type checker:                  BasicChecker
        :param group_name:
        :type group_name:               str
        :return:                        None
        """
        self._checkers[group_name]['checkers'].append((checker, is_relative))

    def add_pos(self, pos):
        self._pos[0] += pos[0]
        self._pos[1] += pos[1]
        for group in self._checkers:
            for checker in self._checkers[group]['checkers']:
                checker: BasicChecker
                checker.add_pos(pos)


class BasicPage(object):
    def __init__(self):
        self._button_trusteeship: List[BasicButton] = []
        self._surface_trusteeship: List[BasicSurface] = []
        self._page_trusteeship: List[BasicPage] = []
        self.cp = []

    def change_blit_pos(self, pos):
        """
        :param pos:         更改后的坐标
        :type pos:          (int, int) | List[int]
        :return:
        """
        pass

    def in_area(self, mouse_pos):
        pass

    def set_as_background(self):
        pass

    def add_button_trusteeship(self, button: BasicButton):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__name__))
        self._button_trusteeship.append(button)

    def show_button_trusteeship(self):
        return self._button_trusteeship

    def add_surface_trusteeship(self, surface: BasicSurface):
        if not isinstance(surface, BasicSurface):
            raise UnexpectedParameter(error0x02.format(BasicSurface.__name__))
        self._surface_trusteeship.append(surface)

    def show_surface_trusteeship(self):
        return self._surface_trusteeship

    def add_page_trusteeship(self, page):
        """
        :type page:                     BasicPage
        :return:
        """
        if not isinstance(page, BasicPage):
            raise UnexpectedParameter(error0x02.format(BasicPage.__name__))
        self._page_trusteeship.append(page)

    def show_page_trusteeship(self):
        return self._page_trusteeship

    def operate(self, mouse_pos, effectiveness, mouse_wheel_status=None, operate_addons=False, mouse_press=None):
        pass


class BasicInputBox:
    def __init__(self, size, pos, surface, default_text='', remind_text='', background_color=(255, 255, 255), border_color=((0, 0, 0), (0, 112, 255)),
                 font_color=(0, 0, 0), font_type='SimHei', font_size=20, remind_text_color=(160, 160, 160), border_width=2, border_radius=1, fps=60,
                 cursor_color=(0, 0, 0), select_area_color=((51, 103, 209), (200, 200, 200)), do_color_reverse=True):
        """
        :param size:                    输入框大小
        :type size:                     List[int] | Tuple[int]
        :param pos:                     输入框位置
        :type pos:                      List[int] | Tuple[int]
        :param surface:                 输入框将位于哪个表面（相对位置）
        :type surface:                  pygame.SurfaceType
        :param default_text:            初始文字
        :type default_text:             str
        :param remind_text:             提示词
        :type remind_text:              str
        :param background_color:        背景色
        :type background_color:         List[int] | Tuple[int, int, int]
        :param border_color:            边框颜色
        :type border_color:             List[int] | Tuple[int, int, int]
        :param font_color:              文字颜色
        :type font_color:               List[int] | Tuple[int, int, int]
        :param font_type:               字体（路径或名称）
        :type font_type:                str
        :param font_size:               字体大小
        :type font_size:                int
        :param remind_text_color:       提示词颜色
        :type remind_text_color:        List[int] | Tuple[int, int, int]
        :param border_width:            边框宽度
        :type border_width:             int
        :param border_radius:           边框圆角半径
        :type border_radius:            int
        :param fps:                     屏幕刷新频率
        :type fps:                      int
        :param cursor_color:            光标颜色
        :type cursor_color:             List[int] | Tuple[int, int, int]
        :param select_area_color:       选区颜色
        :type select_area_color:        List[int] | Tuple[int, int, int]
        :param do_color_reverse:        选区颜色是否反色
        :type do_color_reverse:         bool
        """
        self.size = size
        self.pos = pos
        self.rect = pygame.Rect(*pos, *size)
        self.screen = surface
        self.surface = pygame.Surface(size).convert_alpha()
        self.background = None
        self.text = default_text
        self.remind_text = remind_text
        self.background_color = background_color
        self.border_color = border_color
        self.font_color = font_color
        self.font_type = font_type
        self.font_size = font_size
        if os.path.exists(font_type):
            self.font_family = pygame.font.Font(font_type, font_size)
        else:
            self.font_family = pygame.font.SysFont(font_type, font_size)
        self.remind_text_color = remind_text_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.fps = fps
        self.cursor_color = cursor_color
        self.dragging = False
        self.surface.fill((0, 0, 0, 0))
        self.select_area_color = select_area_color
        self.do_color_reverse = do_color_reverse

    def set_as_background(self):
        self.background = self.surface.copy()

    def in_area(self, mouse_pos):
        return self.rect.collidepoint(*mouse_pos)

    def handel(self, event_r: pygame.event.Event):
        pass

    def operate(self, mouse_pos, mouse_press):
        """
        :param mouse_pos:               鼠标坐标（相对目标表面）
        :type mouse_pos:                List[int] | Tuple[int, int]
        :param mouse_press:             鼠标状态（左键，中键，右键）
        :type mouse_press:              List[bool] | Tuple[bool, bool, bool]
        :return:
        """
        pass


class BasicPopup:
    def __init__(self, size, pos, screen):
        """
        :param size:                    弹出框大小
        :type size:                     List[int] | Tuple[int, int]
        :param pos:                     弹出框位置
        :type pos:                      List[int] | Tuple[int, int]
        :param screen:                  要显示在哪个 Surface 上
        :type screen:                   pygame.SurfaceType
        """
        self.clock = pygame.time.Clock()
        self.size = size
        self.pos = pos
        self.screen = screen
        self.surface = pygame.Surface(self.size)

    def show(self):
        pass

    def loop(self, function, args):
        pass
