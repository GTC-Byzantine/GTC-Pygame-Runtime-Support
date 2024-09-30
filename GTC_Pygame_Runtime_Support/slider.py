import pygame
import sys


#####
class Slider:

    def __init__(self, background: pygame.Surface, acceleration: float, surface: pygame.Surface,
                 direction: tuple[int, int] = (1, 0), initial_speed: int = 5, previous_image=None,
                 slide_with=False, screen_background=None):
        self.size = surface.get_size()
        self.image = pygame.transform.scale(background, self.size)
        self.acceleration = acceleration
        self.speed: float = 0
        self.surface = surface
        if not isinstance(direction, tuple) or direction[0] not in [-1, 0, 1] or direction[1] not in [-1, 0, 1]:
            raise TypeError('666 不看文档嘛')
        self.start_pos = [direction[0] * self.size[0], direction[1] * self.size[1]]
        self.speed_vector = [-direction[0], -direction[1]]
        self.initial_speed = initial_speed
        self.speed = [0, 0]
        self.acceleration = acceleration
        self.pos = self.start_pos.copy()
        self.image_status = previous_image
        self.do_slide = slide_with
        self.background = pygame.transform.scale(screen_background, self.size)
        if isinstance(self.image_status, pygame.Surface):
            self.image_status = pygame.transform.scale(self.image_status, self.size)

    def next_frame(self):

        if abs(self.pos[0] + self.speed[0]) <= 10 and abs(self.pos[1] + self.speed[1]) <= 10:
            return True
        else:
            self.surface.fill((255, 255, 255))
            if self.background is not None:
                self.surface.blit(self.background, (0, 0))
            if self.image_status is not None:
                if self.do_slide:
                    self.surface.blit(self.image_status, (self.pos[0] - self.size[0], self.pos[1] - self.size[1]))
                else:
                    self.surface.blit(self.image_status, (0, 0))
            for i in [0, 1]:
                self.speed[i] += self.speed_vector[i] * self.acceleration
                self.pos[i] += self.speed[i]
            self.surface.blit(self.image, self.pos)
            print(self.pos)
            pygame.display.flip()
        return False
#####
