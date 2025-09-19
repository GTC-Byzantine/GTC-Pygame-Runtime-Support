# GTC Pygame Runtime Support
集成 Pygame 应用开发支持

Finding an English version? [click here](https://github.com/GTC-Software-Studio/GTC-Pygame-Runtime-Support)

нашли русскую версию? [кликните сюда](https://github.com/GTC-Software-Studio/GTC-Pygame-Runtime-Support/blob/main/README-ru.md)

## 软件包安装
向绝大多数软件包一样，本软件包也可使用 pip 下载并安装

```plain
pip install GTC_Pygame_Runtime_Support
```

如果 pip 不慎爆炸，您可以从 [Github](https://github.com/GTC-Byzantine/GTC-Pygame-Runtime-Support/) 处直接复制源码

## 使用示例
### 按钮
PRS 提供三种按钮类型，全部位于`button.py`文件内，此处以其中的`FeedbackButton`为例进行展示

```python
import pygame
import GTC_Pygame_Runtime_Support as gPRS
screen = pygame.display.set_mode((200, 200))
button = gPRS.button.FeedbackButton([40, 40], [20, 20], '114', 15, screen, bg_color=[0, 145, 220], 
                                    border_color=[209, 240, 255], text_color=[255, 255, 255],
                                    change_color=((0, 145, 220), (0, 225, 0))) # 生成按钮
running = 1
clock = pygame.time.Clock()
while running: # 主循环
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    button.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)) # 按钮贴图处
    if button.on_click:
        print("clicked")
    pygame.display.flip()
    clock.tick(60)
```

运行如上代码，你将能够创建一个显示文字为 114 的按钮，并且点击这个按钮后，控制台会输出"clicked"，并且根据用户的动作，按钮将会有不同的反馈。

### 页面
PRS 提供的页面类型位于`page.py`内，此处以`PlainPage`为例进行展示

```python
import sys
import pygame
import GTC_Pygame_Runtime_Support as gPRS

screen = pygame.display.set_mode((500, 500))
bp = gPRS.page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()

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
        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3), mw, True)
        pygame.display.flip()
        clock.tick(60)
```

运行上述代码，你将能够创建一个可由鼠标滚轮滚动和鼠标左键拖动的页面，你可以自行更换其背景，只要你在主循环前调用函数`bp.set_as_background()`

### PRS 中的嵌套操作
在 PRS 中，一切展示型组件都可通过托管 (trusteeship) 的方式进行嵌套。

#### 在页面中嵌套按钮
PRS 中所有组件托管按钮的方式均相同，就像下面展示的：

```python
import sys
import pygame
import GTC_Pygame_Runtime_Support as gPRS

screen = pygame.display.set_mode((500, 500))
bp = gPRS.page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()
    bt = gPRS.button.FeedbackButton([40, 40], [20, 20], '114', 10, bp.surface)
    bp.add_module_trusteeship(bt)

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
        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3), mw, True)
        if bt.on_click:
            print('clicked')
        pygame.display.flip()
        clock.tick(60)
```

PRS 通常通过`item.add_button_trusteeship(button)`的形式添加嵌套按钮，同时按钮声明时的目标 surface 应指向被嵌套对象的 surface，通常是`item.surface`。

#### 在页面中嵌套页面
原理基本同上。

```python
import sys
import pygame
import GTC_Pygame_Runtime_Support as gPRS

screen = pygame.display.set_mode((500, 500))
bp = gPRS.page.PlainPage([300, 300], [300, 1000], [100, 100], screen, 1.4, True)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    bp.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(bp.surface, [0, 0, 0], [0, 10 * i], [300, 10 * i])
    bp.set_as_background()
    inner_p = gPRS.page.PlainPage([100, 100], [100, 300], [50, 200], bp.surface, wheel_support=True)
    inner_p.surface.fill((255, 255, 255))
    for i in range(100):
        pygame.draw.line(inner_p.surface, [0, 0, 255], [0, 9 * i], [300, 9 * i])
    inner_p.set_as_background()
    bp.add_module_trusteeship(inner_p)

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
        bp.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3), mw, True)
        pygame.display.flip()
        clock.tick(60)
```

通过以上介绍，您应该能对 PRS 的使用特点有大概的了解。

该页面不仅可以使用滚轮滚动页面，也可以使用鼠标拖动页面，并且在使用`add_module_trusteeship()`函数后，按钮也可以正常使用。

所有功能组件的 Surface 图层均向开发者开放，这使得开发者在不满意原按钮的美术效果时可以自行修改图层，比如上例中向滚动页面绘制直线，使用者可以直接通过`bp.surface`获得页面的 Surface，并通过`bp.set_as_background()`方便地设置其为默认背景。
