import pygame
from GTC_Pygame_Runtime_Support.basic_class import BasicPopup
from GTC_Pygame_Runtime_Support.return_type import user_quit


class SimplePopup(BasicPopup):
    def __init__(self, size, pos, screen, start_pos):
        """
        :param start_pos:               动画起始位置
        :type start_pos                 List[int] | Tuple[int, int]
        """
        super().__init__(size, pos, screen)
        self.start_pos = start_pos

    def animation(self, fps, acc, func=None) -> str:
        """
        :param fps:                     窗口真实刷新率
        :type fps:                      int
        :param acc:                     动画速度
        :type acc:                      float | int
        :param func:                    执行函数
        :type func:                     function
        :return:                        None
        """
        background = self.screen.copy()
        clock = pygame.time.Clock()
        shadow = pygame.Surface(self.screen_size).convert_alpha()
        shadow.fill((127, 127, 127))
        for i in range(0, 128, 6 * 60 // fps):
            for event_r in pygame.event.get():
                if event_r.type == pygame.QUIT:
                    return user_quit

            shadow.set_alpha(i)
            self.screen.blit(background, (0, 0))
            self.screen.blit(shadow, (0, 0))
            pygame.display.flip()
            clock.tick(fps)

        alpha = 0
        delta_pos = [self.start_pos[0] - self.pos[0], self.start_pos[1] - self.pos[1]]
        real_pos = [*self.start_pos]
        t = 0
        while not (abs(delta_pos[0]) <= 2 and abs(delta_pos[1]) <= 2):
            delta_pos[0] /= acc
            delta_pos[1] /= acc
            t += 1
        c = 0
        while True:
            for event_r in pygame.event.get():
                if event_r.type == pygame.QUIT:
                    return user_quit

            self.surface.fill((255, 255, 255))
            if self.background is not None:
                self.surface.blit(self.background, (0, 0))

            for i in range(2):
                real_pos[i] = (real_pos[i] - self.pos[i]) / acc + self.pos[i]
            if abs(real_pos[0] - self.pos[0]) <= 2 and abs(real_pos[1] - self.pos[1]) <= 2:
                break

            for sur in self.surface_trusteeship:
                sur[0]: pygame.Surface
                sur[0].set_alpha(255 * c // t)
                self.surface.blit(sur[0], [sur[1][0] + real_pos[0] - self.pos[0], sur[1][1] + real_pos[1] - self.pos[1]])

            self.screen.blit(background, (0, 0))
            self.screen.blit(shadow, (0, 0))
            self.screen.blit(self.surface, real_pos)
            pygame.display.flip()
            clock.tick(fps)
            c += 1
        if func is not None:
            func()
        while True:
            for event_r in pygame.event.get():
                if event_r.type == pygame.QUIT:
                    return user_quit

            self.surface.fill((255, 255, 255))
            if self.background is not None:
                self.surface.blit(self.background, (0, 0))

            for i in range(2):
                real_pos[i] = (real_pos[i] - self.start_pos[i]) / acc + self.start_pos[i]
            if abs(real_pos[0] - self.start_pos[0]) <= 2 and abs(real_pos[1] - self.start_pos[1]) <= 2:
                break

            for sur in self.surface_trusteeship:
                sur[0]: pygame.Surface
                sur[0].set_alpha(255 * c // t)
                self.surface.blit(sur[0], [sur[1][0] + real_pos[0] - self.pos[0], sur[1][1] + real_pos[1] - self.pos[1]])

            self.screen.blit(background, (0, 0))
            self.screen.blit(shadow, (0, 0))
            self.screen.blit(self.surface, real_pos)
            pygame.display.flip()
            clock.tick(fps)
            c -= 1
        for i in range(128, 0, -6 * 60 // fps):
            for event_r in pygame.event.get():
                if event_r.type == pygame.QUIT:
                    return user_quit

            shadow.set_alpha(i)
            self.screen.blit(background, (0, 0))
            self.screen.blit(shadow, (0, 0))
            pygame.display.flip()
            clock.tick(fps)

    def show(self):
        self.screen.blit(self.surface, self.pos)

    def loop(self, function, args):
        function(*args)


if __name__ == '__main__':
    sc = pygame.display.set_mode((500, 500))
    sc.fill((255, 255, 255))
    sp = SimplePopup([200, 200], [150, 150], sc, [-200, -100])
    sp.add_surface_trusteeship(pygame.Surface((100, 100)).convert_alpha(), [50, 50])
    sp.animation(60, 1.05)
