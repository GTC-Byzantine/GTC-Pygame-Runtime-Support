import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicChecker, BasicSurface
from GTC_Pygame_Runtime_Support.checker import AlwaysTrue

class CommonSurface(BasicSurface):
    def __init__(self, size, pos, screen):
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface(size)
        self.screen = screen
        self.checkers = {}

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
        :return:                        none
        """
        self.checkers[group_name] = {'checkers': [], 'motion': motion, 'args':args, 'type': checker_type}
    def add_checker(self, group_name, checker):
        """
        :param checker:
        :type checker:                  BasicChecker
        :param group_name:
        :type group_name:               str
        :return:
        """
        self.checkers[group_name]['checkers'].append(checker)

    def run_check(self, mouse_pos, mouse_click):
        """
        :param mouse_pos:
        :type mouse_pos:                        (int, int) | List[int]
        :param mouse_click:
        :type mouse_click:                      (bool, bool, bool, bool, bool) | List[int]
        :return:
        """
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

    def add_pos(self, pos):
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]
        for group in self.checkers:
            for checker in self.checkers[group]['checkers']:
                checker:BasicChecker
                checker.add_pos(pos)

if __name__ == '__main__':
    s = CommonSurface([30, 30], [10, 10], None)
    s.add_checker_group('1', print, ['114514s', '1919810'], 'and')
    s.add_checker('1', AlwaysTrue([10, 10, 30, 30], False))
    s.add_checker('1', AlwaysTrue([10, 10, 30, 30], False))
    s.run_check([0, 0], [True])
    # s.operate([0, 0], [True])
