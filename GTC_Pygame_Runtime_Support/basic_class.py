from typing import List
import pygame
from pygame import SurfaceType
from GTC_Pygame_Runtime_Support.error import UnexpectedParameter, error0x02

pygame.display.init()


class BasicButton(object):
    state = False

    def __init__(self):
        self.do_cancel = False

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

    def add_button_trusteeship(self, button: BasicButton):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__class__.__name__))
        self._button_trusteeship.append(button)
        self.do_element_show.append(False)

    def operate_button(self, mouse_pos, effectiveness, do_cancel):
        for button in self._button_trusteeship:
            if self.do_element_show[self._button_trusteeship.index(button)]:
                button.operate(mouse_pos, effectiveness)
                if do_cancel:
                    button.cancel()

    def operate(self, mouse_pos, effectiveness, do_cancel=False):
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
            raise UnexpectedParameter(error0x02.format(BasicButton.__class__.__name__))
        self._button_trusteeship.append(button)

    def add_surface_trusteeship(self, surface: BasicSurface):
        if not isinstance(surface, BasicSurface):
            raise UnexpectedParameter(error0x02.format(BasicSurface.__class__.__name__))
        self._surface_trusteeship.append(surface)

    def add_page_trusteeship(self, page):
        """
        :type page:                     BasicPage
        :return:
        """
        if not isinstance(page, BasicPage):
            raise UnexpectedParameter(error0x02.format(BasicPage.__class__.__name__))
        self._page_trusteeship.append(page)

    def operate(self, mouse_pos, effectiveness, mouse_wheel_status=None, operate_addons=False, mouse_press=None):
        pass
