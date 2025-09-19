import os

import GTC_Pygame_Runtime_Support
from GTC_Pygame_Runtime_Support.basic_class import BasicAdjustBox, BasicButton
from GTC_Pygame_Runtime_Support.supported_types import *
from GTC_Pygame_Runtime_Support.button import FeedbackButton
from typing import List, Tuple, Union


class SimpleAdjustBox(BasicAdjustBox):
    def __init__(self, size: Coordinate, pos: Coordinate, screen: pygame.Surface, default_value=0, font_type: str = 'SimHei', font_size: int = -1,
                 font_color: ColorValue = (0, 0, 0), adjust_step: Union[List[float], Tuple[float]] = (5, 50),
                 background_color: ColorValue = (255, 255, 255), button_color=(0, 123, 200)):
        super().__init__(size, pos, screen)
        self.adjust_step = adjust_step
        self.font_size = font_size
        if font_size == -1:
            self.font_size = int(size[1] * 0.618)
        if os.path.exists(font_type):
            self.font = pygame.font.Font(font_type, self.font_size)
        else:
            self.font = pygame.font.SysFont(font_type, self.font_size)
        self.font_type = font_type
        self.font_color = font_color
        self.surface = pygame.Surface(size).convert_alpha()
        self.bg_color = background_color
        self.buttons: List[List[BasicButton]] = []
        self.value = default_value
        self.last_value = None
        self.text_sur = None
        self.text_rect = None
        self.text = ''
        for step in adjust_step:
            self.buttons.append([])
            self.buttons[-1].append(
                FeedbackButton([size[1], size[1]], [0, 0], '-' + str(step), self.font_size, screen, font_type=font_type, bg_color=button_color,
                               border_color=button_color, text_color=font_color))
            self.buttons[-1][-1].is_base_module = False
            self.buttons[-1].append(
                FeedbackButton([size[1], size[1]], [0, 0], '+' + str(step), self.font_size, screen, font_type=font_type, bg_color=button_color,
                               border_color=button_color, text_color=font_color))
            self.buttons[-1][-1].is_base_module = False

    def operate(self, mouse_pos, mouse_press):
        self.in_active = False
        self.surface.fill((0, 0, 0, 0))
        if self.is_base_module:
            self.absolute_pos = self.pos
        pygame.draw.rect(self.surface, self.bg_color, [0, 0, *self.size], border_radius=self.size[1] // 4)
        if self.last_value is None or self.last_value != self.value:
            self.text_sur = self.font.render(str(self.value), 1, self.font_color)
            self.text_rect = self.text_sur.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
            self.last_value = self.value
            self.in_active = True
        self.surface.blit(self.text_sur, self.text_rect)
        self._screen.blit(self.surface, self.pos)
        if self.in_active:
            GTC_Pygame_Runtime_Support.refresh_stuck[(*self.absolute_pos, *self.size)] = 1
        for i in range(len(self.buttons)):
            self.buttons[i][0].change_pos([self.pos[0] - (i + 1) * (self.size[1] + 5), self.pos[1]])
            self.buttons[i][0].absolute_pos = [self.absolute_pos[0] - (i + 1) * (self.size[1] + 5), self.absolute_pos[1]]
            self.buttons[i][1].change_pos([self.pos[0] + self.size[0] + 5 + i * (self.size[1] + 5), self.pos[1]])
            self.buttons[i][1].absolute_pos = [self.absolute_pos[0] + self.size[0] + 5 + i * (self.size[1] + 5), self.absolute_pos[1]]
            for t in [0, 1]:
                self.buttons[i][t].operate(mouse_pos, mouse_press)
                if self.buttons[i][t].on_click:
                    if t:
                        self.value += self.adjust_step[i]
                    else:
                        self.value -= self.adjust_step[i]  # print(self.value)
        self.text = str(self.value)


if __name__ == '__main__':
    sc = pygame.display.set_mode((800, 600))
    sab = SimpleAdjustBox([300, 50], [250, 200], sc)
    clock = pygame.time.Clock()
    while True:
        sc.fill((220, 220, 220))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sab.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        pygame.display.flip()
        clock.tick(60)
