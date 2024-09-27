import sys
import pygame
import button_support
import basic_page

screen = pygame.display.set_mode((500, 500))
bp = basic_page.BasicPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    mw = [False, False]
    while True:
        mw = [False, False]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    mw[1] = True
                elif event.button == 5:
                    mw[0] = True

        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0], mw)
        pygame.display.flip()
        clock.tick(60)
