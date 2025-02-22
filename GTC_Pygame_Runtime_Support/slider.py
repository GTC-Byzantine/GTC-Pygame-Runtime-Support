import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicSlider
from GTC_Pygame_Runtime_Support.error import UnexpectedParameter


class HorizontalSlider(BasicSlider):
    def __init__(self, size, pos, screen, movable_radium, drag_index=0, movable_color=(18, 107, 174), background_color=(255, 255, 255)):
        super().__init__(size, pos, screen)
        self.movable_radium = movable_radium
        self._drag_index = drag_index
        self._start_pos = None
        self._pre_clicked = False
        self.slide_pos = 0
        self.slide_range = [0, size[0] - size[1]]
        if self.slide_range[1] < 0:
            raise UnexpectedParameter("size[0] 应大于等于 {}, 实际为 {}".format(size[1], size[0]))
        self.movable_color = movable_color
        self.background_color = background_color

    def operate(self, mouse_pos, mouse_press):
        if self.in_area(mouse_pos) or self.sliding:
            if self._lock:
                if not mouse_press[self._drag_index]:
                    self._lock = False
            else:
                if not self._pre_clicked and mouse_press[self._drag_index]:
                    self._start_pos = mouse_pos
                    self.sliding = False
                    self._lock = False
                elif self._pre_clicked and mouse_press[self._drag_index]:
                    if mouse_pos != self._start_pos:
                        self.sliding = True
                    self.slide_pos = mouse_pos[0] - self._pos[0] - self._size[1] // 2
                    self.slide_pos = max(0, self.slide_pos)
                    self.slide_pos = min(self.slide_range[1], self.slide_pos)
                elif self._pre_clicked and not mouse_press[self._drag_index]:
                    self.sliding = False
        else:
            if mouse_press[self._drag_index]:
                self._lock = True
            else:
                self._lock = False

        self._pre_clicked = mouse_press[self._drag_index]
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.background_color, (0, 0, *self._size), border_radius=self._size[1])
        if self.background is not None:
            self.surface.blit(self.background, (0, 0))
        self.percent = self.slide_pos / (self.slide_range[1] - self.slide_range[0])
        self._screen.blit(self.surface, self._pos)
        pygame.draw.circle(self._screen, self.movable_color, (self._size[1] // 2 + self.slide_pos + self._pos[0], self._size[1] // 2 + self._pos[1]),
                           self.movable_radium)


class VerticalSlider(BasicSlider):
    def __init__(self, size, pos, screen, movable_radium, drag_index=0, movable_color=(18, 107, 174), background_color=(255, 255, 255)):
        super().__init__(size, pos, screen)
        self.movable_radium = movable_radium
        self._drag_index = drag_index
        self._start_pos = None
        self._pre_clicked = False
        self.slide_pos = 0
        self.slide_range = [0, size[1] - size[0]]
        if self.slide_range[1] < 0:
            raise UnexpectedParameter("size[1] 应大于等于 {}, 实际为 {}".format(size[0], size[1]))
        self.movable_color = movable_color
        self.background_color = background_color

    def operate(self, mouse_pos, mouse_press):
        if self.in_area(mouse_pos) or self.sliding:
            if self._lock:
                if not mouse_press[self._drag_index]:
                    self._lock = False
            else:
                if not self._pre_clicked and mouse_press[self._drag_index]:
                    self._start_pos = mouse_pos
                    self.sliding = False
                    self._lock = False
                elif self._pre_clicked and mouse_press[self._drag_index]:
                    if mouse_pos != self._start_pos:
                        self.sliding = True
                    self.slide_pos = mouse_pos[1] - self._pos[1] - self._size[0] // 2
                    self.slide_pos = max(0, self.slide_pos)
                    self.slide_pos = min(self.slide_range[1], self.slide_pos)
                elif self._pre_clicked and not mouse_press[self._drag_index]:
                    self.sliding = False
        else:
            if mouse_press[self._drag_index]:
                self._lock = True
            else:
                self._lock = False

        self._pre_clicked = mouse_press[self._drag_index]
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.background_color, (0, 0, *self._size), border_radius=self._size[1])
        if self.background is not None:
            self.surface.blit(self.background, (0, 0))
        self.percent = self.slide_pos / (self.slide_range[1] - self.slide_range[0])
        self._screen.blit(self.surface, self._pos)
        pygame.draw.circle(self._screen, self.movable_color, (self._size[0] // 2 + self._pos[0], self._size[0] // 2 + self.slide_pos + self._pos[1]),
                           self.movable_radium)


class HorizontalSlideBar(BasicSlider):
    def __init__(self, size, pos, screen, movable_width, drag_index=0, movable_color=((177, 177, 177), (127, 127, 127)),
                 background_color=(255, 255, 255)):
        super().__init__(size, pos, screen)
        self.movable_width = movable_width
        self._drag_index = drag_index
        self._movable_color = movable_color
        self._background_color = background_color
        self._pre_clicked = False
        self.slide_range = [movable_width // 2, size[0] - 2 - movable_width // 2 - size[1]]
        self.slide_pos = self.slide_range[0]
        if self.slide_range[1] < 0:
            raise UnexpectedParameter("size[0] 应大于等于 {}, 实际为 {}".format(movable_width // 2 + 2 + size[1], size[0]))
        self._start_pos = 0
        self._drag_pattern = 0
        self._delta = 0

    def set_movable_width(self, new_width):
        self.movable_width = new_width
        self.slide_range = [new_width // 2, self._size[0] - 2 - new_width // 2 - self._size[1]]
        if self.slide_range[1] < 0:
            raise UnexpectedParameter("size[0] 应大于等于 {}, 实际为 {}".format(new_width // 2 + 2 + self._size[1], self._size[0]))

    def operate(self, mouse_pos, mouse_press):
        if self.in_area(mouse_pos) or self.sliding:
            if self._lock:
                if not mouse_press[self._drag_index]:
                    self._lock = False
            else:
                if not self._pre_clicked and mouse_press[self._drag_index]:
                    self._start_pos = mouse_pos
                    self.sliding = False
                    self._lock = False
                    if (self.slide_pos - self.movable_width // 2 <= mouse_pos[0] - self._pos[0]
                            <= self.slide_pos + self.movable_width // 2 + self._size[1]):
                        self._drag_pattern = 1
                    else:
                        self._drag_pattern = 2
                elif self._pre_clicked and mouse_press[self._drag_index]:
                    if mouse_pos != self._start_pos:
                        self.sliding = True
                    if self._drag_pattern == 2:
                        self.slide_pos = mouse_pos[0] - self._pos[0] - self._size[1] // 2
                    elif self._drag_pattern == 1:
                        self.delta = mouse_pos[0] - self._start_pos[0]
                        self.delta = max(self.delta, self.slide_range[0] - self.slide_pos)
                        self.delta = min(self.delta, self.slide_range[1] - self.slide_pos)
                    self.slide_pos = max(self.slide_range[0], self.slide_pos)
                    self.slide_pos = min(self.slide_range[1], self.slide_pos)
                elif self._pre_clicked and not mouse_press[self._drag_index]:
                    self.sliding = False
                    self.slide_pos += self.delta
                    self.delta = 0
        else:
            if mouse_press[self._drag_index]:
                self._lock = True
            else:
                self._lock = False

        self.slide_pos = max(self.slide_range[0], self.slide_pos)
        self.slide_pos = min(self.slide_range[1], self.slide_pos)
        self._pre_clicked = mouse_press[self._drag_index]
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self._background_color, (0, 0, *self._size), border_radius=self._size[1] // 2)
        if self.background is not None:
            self.surface.blit(self.background, (0, 0))
        self.percent = (self.slide_pos - self.slide_range[0] + self.delta) / (self.slide_range[1] - self.slide_range[0])
        self._screen.blit(self.surface, self._pos)
        pygame.draw.rect(self._screen, self._movable_color[self.in_area(mouse_pos) or self.sliding],
                         (self.slide_pos + self._pos[0] + 1 - self.movable_width // 2 + self.delta,
                          self._pos[1] + 1, self.movable_width + self._size[1],
                          self._size[1] - 2), border_radius=(self._size[1] - 2) // 2)


class VerticalSlideBar(BasicSlider):
    def __init__(self, size, pos, screen, movable_width, drag_index=0, movable_color=((177, 177, 177), (127, 127, 127)),
                 background_color=(255, 255, 255)):
        super().__init__(size, pos, screen)
        self.movable_width = movable_width
        self._drag_index = drag_index
        self._movable_color = movable_color
        self._background_color = background_color
        self._pre_clicked = False
        self.slide_range = [movable_width // 2, size[1] - 2 - movable_width // 2 - size[0]]
        self.slide_pos = self.slide_range[0]
        if self.slide_range[1] < 0:
            raise UnexpectedParameter("size[1] 应大于等于 {}, 实际为 {}".format(movable_width // 2 + 2 + size[0], size[1]))
        self._start_pos = 0
        self._drag_pattern = 0
        self._delta = 0

    def set_movable_width(self, new_width):
        self.movable_width = new_width
        self.slide_range = [new_width // 2, self._size[1] - 2 - new_width // 2 - self._size[0]]
        if self.slide_range[1] < 0:
            raise UnexpectedParameter("size[1] 应大于等于 {}, 实际为 {}".format(new_width // 2 + 2 + self._size[0], self._size[1]))

    def operate(self, mouse_pos, mouse_press):
        if self.in_area(mouse_pos) or self.sliding:
            if self._lock:
                if not mouse_press[self._drag_index]:
                    self._lock = False
            else:
                if not self._pre_clicked and mouse_press[self._drag_index]:
                    self._start_pos = mouse_pos
                    self.sliding = False
                    self._lock = False
                    if (self.slide_pos - self.movable_width // 2 <= mouse_pos[1] - self._pos[1]
                            <= self.slide_pos + self.movable_width // 2 + self._size[0]):
                        self._drag_pattern = 1
                    else:
                        self._drag_pattern = 2
                elif self._pre_clicked and mouse_press[self._drag_index]:
                    if mouse_pos != self._start_pos:
                        self.sliding = True
                    if self._drag_pattern == 2:
                        self.slide_pos = mouse_pos[1] - self._pos[1] - self._size[0] // 2
                    elif self._drag_pattern == 1:
                        self.delta = mouse_pos[1] - self._start_pos[1]
                        self.delta = max(self.delta, self.slide_range[0] - self.slide_pos)
                        self.delta = min(self.delta, self.slide_range[1] - self.slide_pos)
                    self.slide_pos = max(self.slide_range[0], self.slide_pos)
                    self.slide_pos = min(self.slide_range[1], self.slide_pos)
                elif self._pre_clicked and not mouse_press[self._drag_index]:
                    self.sliding = False
                    self.slide_pos += self.delta
                    self.delta = 0
        else:
            if mouse_press[self._drag_index]:
                self._lock = True
            else:
                self._lock = False
        self.slide_pos = max(self.slide_range[0], self.slide_pos)
        self.slide_pos = min(self.slide_range[1], self.slide_pos)
        self._pre_clicked = mouse_press[self._drag_index]
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self._background_color, (0, 0, *self._size), border_radius=self._size[0] // 2)
        if self.background is not None:
            self.surface.blit(self.background, (0, 0))
        self.percent = (self.slide_pos - self.slide_range[0] + self.delta) / (self.slide_range[1] - self.slide_range[0])
        self._screen.blit(self.surface, self._pos)
        pygame.draw.rect(self._screen, self._movable_color[self.in_area(mouse_pos) or self.sliding],
                         (self._pos[0] + 1, self.slide_pos + self._pos[1] + 1 - self.movable_width // 2 + self.delta,
                          self._size[0] - 2,
                          self.movable_width + self._size[0]), border_radius=(self._size[0] - 2) // 2)


if __name__ == '__main__':
    sc = pygame.display.set_mode((500, 500))
    hs = HorizontalSlider([200, 60], [150, 200], sc, 40)
    vs = VerticalSlider([60, 200], [100, 300], sc, 40)
    hsb = HorizontalSlideBar([200, 10], [100, 20], sc, 60)
    vsb = VerticalSlideBar([10, 500], [490, 0], sc, 60)
    hsb.set_movable_width(100)
    vsb.set_movable_width(120)
    running = 1
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
        sc.fill((0, 0, 0))
        hs.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        vs.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        hsb.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        vsb.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        if vsb.sliding:
            print(vsb.percent)
        if hsb.sliding:
            print(hsb.percent)
        pygame.display.flip()
        clock.tick(60)
