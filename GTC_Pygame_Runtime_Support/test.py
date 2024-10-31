import sys
import pygame
import button_support
import basic_page

screen = pygame.display.set_mode((500, 500))
bp = basic_page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()
    bp.add_button_trusteeship(button_support.FeedbackButton([280, 80], (0, 0), '课堂小记', 62, bp.surface,
                                                            bg_color=[0, 145, 220],
                                                            border_color=[209, 240, 255], text_color=(255, 255, 255),
                                                            change_color=((0, 145, 220), (0, 220, 145))))
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

        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0], mw, True)
        # screen.blit(bp._background, (0, 0))
        pygame.display.flip()
        clock.tick(60)
