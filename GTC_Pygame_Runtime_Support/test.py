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

    s = surface.CommonSurface((100, 100), (150, 150), bp.surface)
    inner_p = page.PlainPage([100, 100], [100, 300], [50, 200], bp.surface, wheel_support=True)
    inner_p.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(inner_p.surface, [0, 0, 255], [0, 3 * i], [300, 3 * i])
    inner_p.set_as_background()
    inner_bt = button.FeedbackButton((50, 50), (25, 25), '9', 25, inner_p.surface)
    inner_p.add_button_trusteeship(inner_bt)
    bp.add_page_trusteeship(inner_p)
    bp.add_surface_trusteeship(s)
    bt = button.FeedbackButton((50, 50), (25, 25), '6', 25, s.surface)
    s.add_button_trusteeship(bt)
    def react():
        s.surface.fill((0, 255, 71), (0, 0, 100, 100))
        s.do_element_show[0] = True
    s.add_checker_group('1', react, [], 'and')
    s.add_checker('1', checker.OnHover([0, 0, 100, 100], False), True)
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
        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0], mw, True)
        # screen.blit(bp._background, (0, 0))
        if bt.on_click or inner_bt.on_click:
            print('clicked')
        pygame.display.flip()
        clock.tick(60)
