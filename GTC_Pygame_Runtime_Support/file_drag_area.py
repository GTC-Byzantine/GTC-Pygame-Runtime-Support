import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicFileDropArea
from GTC_Pygame_Runtime_Support.supported_types import *


class FileDropArea(BasicFileDropArea):
    def __init__(self, size: Coordinate, pos: Coordinate, screen: pygame.Surface):
        super().__init__(size, pos, screen)

    def in_area(self, mouse_pos: MousePosType):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + self.pos[1]:
            return True
        return False

    def handel(self, event_r: pygame.event.Event, mouse_pos: MousePosType):
        if event_r.type == pygame.DROPFILE:
            if self.in_area(mouse_pos):
                self.file_path.append(event_r.file)
                self.dropped = True


if __name__ == '__main__':
    sc = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    fda = FileDropArea((500, 500), (200, 200), sc)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            fda.handel(event, pygame.mouse.get_pos())
        if fda.dropped:
            print(fda.file_path)
        fda.clear_state()
        clock.tick(60)
