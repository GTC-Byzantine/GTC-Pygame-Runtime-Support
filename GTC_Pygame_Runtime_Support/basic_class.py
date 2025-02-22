# 感谢 zhy 同学，对本项目提供大力支持，并且是本项目的第一个正式使用者（被迫受虐者）
# 感谢 wxy 同学，对我一直以来的情感支持
# 感谢 kfy 同学，以各种刁钻的角度测试这个运行库
import os
from typing import List, Tuple
import pygame
from pygame import SurfaceType
from GTC_Pygame_Runtime_Support.error import UnexpectedParameter, error0x02

pygame.display.init()


class BasicButton(object):
    state = False

    def __init__(self):
        self.do_cancel = False
        self.cp = []

    def operate(self, mouse_pos, mouse_press):
        """
        :param mouse_pos:
        :type mouse_pos:            (int, int) | List[int]
        :param mouse_press:
        :type mouse_press:          List[bool] | Tuple[bool, bool, bool] | Tuple[bool, bool, bool, bool, bool]
        :return:
        """
        self.do_cancel: bool = False

    def cancel(self):
        self.state = False
        self.do_cancel = True


class BasicSlider(object):
    def __init__(self, size, pos, screen):
        self._size = size
        self._pos = pos
        self._screen = screen
        self.surface = pygame.Surface(size).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        self._lock = False
        self.percent = 0.0
        self.sliding = False
        self.delta = 0
        self.background = None

    def set_as_background(self):
        self.background = self.surface.copy()

    def in_area(self, mouse_pos):
        if self._pos[0] <= mouse_pos[0] <= self._size[0] + self._pos[0] and self._pos[1] <= mouse_pos[1] <= self._size[1] + self._pos[1]:
            return True
        return False

    def operate(self, mouse_pos, mouse_press):
        pass

    def change_pos(self, pos: Tuple[int, int]):
        self._pos = pos


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
        :type mouse_click:                      (bool, bool, bool, bool, bool) | List[int] | (bool, bool, bool)
        :return:                                bool
        """
        pass

    def change_range(self, check_range):
        self.range = check_range

    def add_pos(self, pos):
        self.range[0] = pos[0]
        self.range[1] = pos[1]


class BasicSurface:
    def __init__(self, size, pos, screen, border_radius=0):
        self._size = size
        self._pos = pos
        self.surface: SurfaceType = pygame.Surface(size).convert_alpha()
        self._screen: SurfaceType = screen
        self._checkers = {}
        self._button_trusteeship: List[BasicButton] = []
        self.do_element_show = []
        self._background = None
        self.cp = []
        self.border_radius = border_radius

    def set_as_background(self):
        self._background = self.surface.copy()

    def add_button_trusteeship(self, button: BasicButton):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__name__))
        self._button_trusteeship.append(button)
        self.do_element_show.append(False)

    def show_button_trusteeship(self):
        return self._button_trusteeship

    def operate_button(self, mouse_pos, mouse_press, do_cancel):
        for button in self._button_trusteeship:
            if self.do_element_show[self._button_trusteeship.index(button)]:
                button.operate(mouse_pos, mouse_press)
                if do_cancel:
                    button.cancel()

    def operate(self, mouse_pos, mouse_press, do_cancel=False):
        if self._background is not None:
            self.surface.blit(self._background, (0, 0))
        else:
             pygame.draw.rect(self.surface, (), (0, 0, *self._size), border_radius=self.border_radius)
        self.operate_button([mouse_pos[0] - self._pos[0], mouse_pos[1] - self._pos[1]], mouse_press, do_cancel)
        self._screen.blit(self.surface, self._pos)

    def run_check(self, mouse_pos, mouse_click) -> bool:
        """
        :param mouse_pos:
        :type mouse_pos:                        (int, int) | List[int]
        :param mouse_click:
        :type mouse_click:                      (bool, bool, bool, bool, bool) | List[int] | (bool, bool, bool)
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
        self._input_trusteeship: List[BasicInputBox] = []
        self._slider_trusteeship = []
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

    def add_input_trusteeship(self, input_box):
        self._input_trusteeship.append(input_box)

    def show_input_trusteeship(self):
        return self._input_trusteeship

    def add_slider_trusteeship(self, item):
        self._slider_trusteeship.append(item)

    def show_slider_trusteeship(self):
        return self._slider_trusteeship

    def operate(self, mouse_pos, mouse_press, mouse_wheel_status=None, operate_addons=False):
        pass


class BasicInputBox:
    def __init__(self, size, pos, surface, default_text='', remind_text='', background_color=(255, 255, 255), border_color=((0, 0, 0), (0, 112, 255)),
                 font_color=(0, 0, 0), font_type='SimHei', font_size=20, remind_text_color=(160, 160, 160), border_width=2, border_radius=1, fps=60,
                 cursor_color=(0, 0, 0), select_area_color=((51, 103, 209), (200, 200, 200)), do_color_reverse=True):
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
        :type mouse_press:              List[bool] | Tuple[bool, bool, bool] | (bool, bool, bool, bool, bool)
        :return:
        """
        pass

    def change_pos(self, pos: Tuple[int, int]):
        self.pos = pos


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
        self.surface = pygame.Surface(size).convert_alpha()
        self.background = None
        self.surface_trusteeship: List[Tuple[pygame.Surface, List[int]]] = []
        self.screen_size = [screen.get_width(), screen.get_height()]

    def set_as_background(self):
        self.background = self.surface.copy()

    def add_surface_trusteeship(self, surface: pygame.Surface, final_pos: List[int]):
        self.surface_trusteeship.append((surface, final_pos))

    def animation(self, fps, acc, func=None):
        pass

    def show(self):
        pass

    def loop(self, function, args):
        pass
