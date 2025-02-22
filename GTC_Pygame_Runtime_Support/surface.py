import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicChecker, BasicSurface
from GTC_Pygame_Runtime_Support.checker import AlwaysTrue


class CommonSurface(BasicSurface):
    def __init__(self, size, pos, screen, border_radius=0):
        super().__init__(size, pos, screen, border_radius)

    def run_check(self, mouse_pos, mouse_click):
        for i in range(len(self.do_element_show)):
            self.do_element_show[i] = False
        for groups in self._checkers:
            check_type = 0
            state = False
            if self._checkers[groups]['type'] == 'and':
                check_type = 1
                state = True
            elif self._checkers[groups]['type'] == 'or':
                check_type = 2
                state = False
            for checker in self._checkers[groups]['checkers']:
                checker: (BasicChecker, bool)
                if checker[1]:
                    check_consequence = checker[0].check((mouse_pos[0] - self._pos[0], mouse_pos[1] - self._pos[1]), mouse_click)
                else:
                    check_consequence = checker[0].check(mouse_pos, mouse_click)
                if check_type == 1:
                    state = state and check_consequence
                elif check_type == 2:
                    state = state or check_consequence
            if state:
                self._checkers[groups]["motion"](*self._checkers[groups]['args'])


if __name__ == '__main__':
    sc = pygame.display.set_mode((500, 500))
    s = CommonSurface((30, 30), [10, 10], None)
    s.add_checker_group('1', print, ['114514s', '1919810'], 'and')
    s.add_checker('1', AlwaysTrue([10, 10, 30, 30], False))
    s.add_checker('1', AlwaysTrue([10, 10, 30, 30], False))
    s.run_check([0, 0], [True])
    # s.operate([0, 0], [True])
