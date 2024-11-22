import sys
import pygame
import button
import page
import surface
import checker

screen = pygame.display.set_mode((500, 500))
bp = page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()
    bp.add_button_trusteeship(button
                              .FeedbackButton([280, 80], (0, 0), '课堂小记', 62, bp.surface,
                                              bg_color=[0, 145, 220],
                                              border_color=[209, 240, 255], text_color=(255, 255, 255),
                                              change_color=((0, 145, 220), (0, 220, 145))))

    s = surface.CommonSurface((100, 100), (0, 0), screen)
    bt = button.FeedbackButton((50, 50), (25, 25), '6', 25, s.surface)
    def react():
        s.surface.fill((0, 255, 71), (0, 0, 100, 100))
        bt.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    s.add_checker_group('1', react, [], 'and')
    s.add_checker('1', checker.OnHover([0, 0, 100, 100], False))
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
        s.surface.fill((255, 255, 255))
        s.run_check(pygame.mouse.get_pos(), pygame.mouse.get_pressed(5))
        s.operate()
        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0], mw, True)
        # screen.blit(bp._background, (0, 0))
        pygame.display.flip()
        clock.tick(60)
