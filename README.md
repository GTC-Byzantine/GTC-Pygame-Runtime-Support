# GTC Pygame Runtime Support
集成 Pygame 应用开发支持

Finding an English version? [click here](https://github.com/GTC-Software-Studio/GTC-Pygame-Runtime-Support)

нашли русскую версию? [кликните сюда](https://github.com/GTC-Software-Studio/GTC-Pygame-Runtime-Support/blob/main/README-ru.md)

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

```python3
import sys
import pygame
import GTC_Pygame_Runtime_Support as PRS

screen = pygame.display.set_mode((500, 500))
bp = PRS.page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()
    bp.add_button_trusteeship(PRS.button.FeedbackButton([280, 80], (10, 30), '114514', 62, bp.surface,
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
该页面不仅可以使用滚轮滚动页面，也可以使用鼠标拖动页面，并且在使用`add_button_trusteeship()`函数后，按钮也可以正常使用。

所有功能组件的 Surface 图层均向开发者开放，这使得开发者在不满意原按钮的美术效果时可以自行修改图层，比如上例中向滚动页面绘制直线，使用者可以直接通过`bp.surface`获得页面的 Surface，并通过`bp.set_as_background()`方便地设置其为默认背景。
