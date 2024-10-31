import pygame
from typing import *
import os
from GTC_Pygame_Runtime_Support.basic_class import *


#####
class SimpleButtonWithImage(BasicButton):

    def __init__(self, pos: List[int], surface: pygame.Surface, size: Tuple[int, int] = (200, 200),
                 bg_color: Tuple[int, int, int] or Tuple[int, int, int, int] = (255, 255, 255),
                 hovering_color: Tuple[int, int, int] or Tuple[int, int, int, int] = (249, 249, 249),
                 clicking_color: Tuple[int, int, int] or Tuple[int, int, int, int] = (252, 248, 245),
                 bg_image: pygame.Surface or None = None,
                 text: Tuple[str, Tuple[int, int], int, Tuple[int, int, int]] or None = None,
                 font: str = 'SimHei'):
        super().__init__()
        self.size = size
        self.bg_color = bg_color
        self.hovering = hovering_color
        self.clicking = clicking_color
        self.pos = pos
        self.bg_image = None
        if bg_image is not None:
            self.bg_image = pygame.transform.scale(bg_image, size)
        self.surface = surface
        self.lock = False
        self.state = False
        self.text_ini = text
        self.text_size = None
        self.text_color = None
        self.text_pos = [text[1][0] + pos[0], text[1][1] + pos[1]]
        self.cp = []
        self.last_clicked = False
        self.on_click = False
        if text is not None:
            self.text_size = text[2]
            self.text_color = text[3]
            if os.path.exists(font):
                self.text = pygame.font.Font(font, self.text_size).render(text[0], True, self.text_color)
            else:
                self.text = pygame.font.SysFont(font, self.text_size).render(text[0], True, self.text_color)

    def _in_area(self, mouse_pos: Tuple[int, int] or List[int]):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    def operate(self, mouse_pos: Tuple[int, int], effectiveness: bool or Literal[0, 1]):

        if self._in_area(mouse_pos):
            if effectiveness and not self.lock:
                self.state = True
                if not self.last_clicked:
                    self.do_cancel = False
                    self.last_clicked = True
                pygame.draw.rect(self.surface, self.clicking, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
            else:
                self.state = False
                pygame.draw.rect(self.surface, self.hovering, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
            if self.lock and not effectiveness:
                self.lock = False

        else:
            pygame.draw.rect(self.surface, self.bg_color, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
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
        if self.bg_image is not None:
            self.surface.blit(self.bg_image, self.pos)
        pygame.draw.rect(self.surface, (0, 0, 0), [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         width=2)

        if self.text_ini is not None:
            self.surface.blit(self.text, self.text.get_rect(center=self.text_pos))


#####
