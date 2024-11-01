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
