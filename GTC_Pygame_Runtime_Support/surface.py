import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicChecker

class CommonSurface:
    def __init__(self, size, pos, screen):
        self.size = size
        self.pos = pos
        self.surface = pygame.Surface(size)
        self.screen = screen
        self.checkers = {}
    def add_checker_group(self, group_name, motion, checker_type='and'):
        """
        :param group_name:
        :type group_name:               str
        :param motion:
        :type motion:                   function
        :param checker_type:
        :type checker_type:             str
        :return:                        none
        """
        self.checkers[group_name] = {'checkers': [], 'motion': motion, 'type': checker_type}
    def add_checker(self, group_name, checker):
        """
        :param checker:
        :type checker:                  BasicChecker
        :param group_name:
        :type group_name:               str
        :return:
        """
        self.checkers[group_name]['checkers'].append(checker)

    def operate(self, mouse_pos, mouse_click):
        for groups in self.checkers:
            for checker in self.checkers[groups]['checkers']:
                pass

