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
        self.size = size
        self.pos = pos
        self.surface: SurfaceType = pygame.Surface(size).convert_alpha()
        self.screen: SurfaceType = screen
        self.checkers = {}
        self.button_trusteeship: List[BasicButton] = []
        self.do_element_show = []

    def add_button_trusteeship(self, button: BasicButton):
        if not isinstance(button, BasicButton):
            raise UnexpectedParameter(error0x02.format(BasicButton.__class__.__name__))
        self.button_trusteeship.append(button)
        self.do_element_show.append(False)

    def operate_button(self, mouse_pos, effectiveness, do_cancel):
        for button in self.button_trusteeship:
            if self.do_element_show[self.button_trusteeship.index(button)]:
                button.operate(mouse_pos, effectiveness)
                if do_cancel:
                    button.cancel()

    def operate(self, mouse_pos, effectiveness, do_cancel=False):
        self.operate_button([mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1]], effectiveness, do_cancel)
        self.screen.blit(self.surface, self.pos)

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
        self.checkers[group_name] = {'checkers': [], 'motion': motion, 'args': args, 'type': checker_type}

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
        self.checkers[group_name]['checkers'].append((checker, is_relative))

    def add_pos(self, pos):
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]
        for group in self.checkers:
            for checker in self.checkers[group]['checkers']:
                checker: BasicChecker
                checker.add_pos(pos)
