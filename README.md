# GTC Pygame Runtime Support
集成 Pygame 应用开发支持

此软件包可用于 Pygame 应用开发，包括但不限于游戏、窗体应用，应于版本大于 3.4.0 的 Python 环境中运行。

使用时，你可以像这样导入软件包：

```python
import GTC_Pygame_Runtime_Support as PRS
```

软件包内的每个组件有几乎相同的使用方法和属性，通常是`Class()`表示构造函数，`item.operate()`表示将组件贴图到 Surface。接下来将以一个反馈按钮为例展示以上特点：

```python
import pygame
import GTC_Pygame_Runtime_Support as PRS
screen = pygame.display.set_mode((200, 200))
button = PRS.button_support.FeedbackButton([40, 40], [20, 20], '114', 15, screen, bg_color=[0, 145, 220],
                                           border_color=[209, 240, 255], text_color=[255, 255, 255],
                                           change_color=((0, 145, 220), (0, 225, 0)))
running = 1
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    button.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    pygame.display.flip()
    clock.tick(60)

```
可以发现，几乎所有重要信息都在被定义时传入，故调用时只需要传入鼠标坐标(mouse_pos)和是否点击(effectiveness)即可。

PRS 提供较完备的滚动页面解决方案，可以大幅度节省程序员们的头发：

```python
import sys
import pygame
import GTC_Pygame_Runtime_Support as PRS

screen = pygame.display.set_mode((500, 500))
bp = PRS.basic_page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()
    bp.add_button_trusteeship(PRS.button_support.FeedbackButton([280, 80], (10, 30), '114514', 62, bp.surface,
                                                                bg_color=[0, 145, 220],
                                                                border_color=[209, 240, 255], text_color=(255, 255, 255),
                                                                change_color=((0, 145, 220), (0, 220, 145))))
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
        pygame.display.flip()
        clock.tick(60)
```
