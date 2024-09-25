import pygame
from typing import *
import os
from .basic_class import BasicButton


class SimpleButtonWithImage(BasicButton):

    def __init__(self, pos: List[int], surface: pygame.Surface, size: Tuple[int, int] = (200, 200),
                 bg_color: Tuple[int, int, int] or Tuple[int, int, int, int] = (255, 255, 255),
                 hovering_color: Tuple[int, int, int] or Tuple[int, int, int, int] = (249, 249, 249),
                 clicking_color: Tuple[int, int, int] or Tuple[int, int, int, int] = (252, 248, 245),
                 bg_image: pygame.Surface or None = None,
                 text: Tuple[str, Tuple[int, int], int, Tuple[int, int, int]] or None = None,
                 font: str = 'SimHei'):
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
            else:
                self.lock = False
        if self.bg_image is not None:
            self.surface.blit(self.bg_image, self.pos)
        pygame.draw.rect(self.surface, (0, 0, 0), [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         width=2)

        if self.text_ini is not None:
            self.surface.blit(self.text, self.text.get_rect(center=self.text_pos))


if __name__ == "__main__":
    pygame.init()
    sc = pygame.display.set_mode((500, 500))
    button = SimpleButtonWithImage([50, 100], sc, bg_image=pygame.image.load('../Data/Image/p1.png'),
                                   text=['文件夹', (100, 150), 25, (0, 0, 0)], font='../ddjbt.ttf')
    button1 = SimpleButtonWithImage([300, 100], sc, bg_image=pygame.image.load('../Data/Image/p5.png'),
                                    text=['markdown', (100, 150), 25, (0, 0, 0)], font='../ddjbt.ttf')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.fill((255, 255, 255))
        button.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        button1.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        print(button.state)

        pygame.display.update()
