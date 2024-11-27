import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicChecker, BasicSurface
from GTC_Pygame_Runtime_Support.checker import AlwaysTrue

class CommonSurface(BasicSurface):
    def __init__(self, size, pos, screen):
        super().__init__(size, pos, screen)

    def run_check(self, mouse_pos, mouse_click):
        for groups in self.checkers:
            check_type = 0
            state = False
            if self.checkers[groups]['type'] == 'and':
                check_type = 1
                state = True
            elif self.checkers[groups]['type'] == 'or':
                check_type = 2
                state = False
            for checker in self.checkers[groups]['checkers']:
                if check_type == 1:
                    state = state and checker.check(mouse_pos, mouse_click)
                elif check_type == 2:
                    state = state or checker.check(mouse_pos, mouse_click)
            if state:
                self.checkers[groups]["motion"](*self.checkers[groups]['args'])
    def operate(self):
        self.screen.blit(self.surface, self.pos)

if __name__ == '__main__':
    s = CommonSurface([30, 30], [10, 10], None)
    s.add_checker_group('1', print, ['114514s', '1919810'], 'and')
    s.add_checker('1', AlwaysTrue([10, 10, 30, 30], False))
    s.add_checker('1', AlwaysTrue([10, 10, 30, 30], False))
    s.run_check([0, 0], [True])
    # s.operate([0, 0], [True])
