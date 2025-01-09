import os
import pygame
import ctypes.wintypes as w
import ctypes

os.environ["SDL_IME_SHOW_UI"] = "1"
pygame.init()

CF_UNICODETEXT = 13

u32 = ctypes.WinDLL('user32')
k32 = ctypes.WinDLL('kernel32')

OpenClipboard = u32.OpenClipboard
OpenClipboard.argtypes = w.HWND,
OpenClipboard.restype = w.BOOL
GetClipboardData = u32.GetClipboardData
GetClipboardData.argtypes = w.UINT,
GetClipboardData.restype = w.HANDLE
GlobalLock = k32.GlobalLock
GlobalLock.argtypes = w.HGLOBAL,
GlobalLock.restype = w.LPVOID
GlobalUnlock = k32.GlobalUnlock
GlobalUnlock.argtypes = w.HGLOBAL,
GlobalUnlock.restype = w.BOOL
CloseClipboard = u32.CloseClipboard
CloseClipboard.argtypes = None
CloseClipboard.restype = w.BOOL


def get_clipboard_text():
    text = ""
    if OpenClipboard(None):
        h_clip_mem = GetClipboardData(CF_UNICODETEXT)
        text = ctypes.wstring_at(GlobalLock(h_clip_mem))
        GlobalUnlock(h_clip_mem)
        CloseClipboard()
    return text


class InputBox:

    def __init__(self, size, pos, surface, default_text='', remind_text='', background_color=(255, 255, 255), border_color=((0, 0, 0), (0, 112, 255)),
                 font_color=(0, 0, 0), font_type='SimHei', font_size=20, remind_text_color=(160, 160, 160), border_width=2, border_radius=1, fps=60,
                 cursor_color=(0, 0, 0), select_area_color=((51, 103, 209), (200, 200, 200)), do_color_reverse=True):
        self.size = size
        self.pos = pos
        self.rect = pygame.Rect(*pos, *size)
        self.screen = surface
        self.surface = pygame.Surface(size).convert_alpha()
        self.background = None
        self.text = default_text
        self.remind_text = remind_text
        self.background_color = background_color
        self.border_color = border_color
        self.font_color = font_color
        self.font_type = font_type
        self.font_size = font_size
        if os.path.exists(font_type):
            self.font_family = pygame.font.Font(font_type, font_size)
        else:
            self.font_family = pygame.font.SysFont(font_type, font_size)
        self.remind_text_color = remind_text_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.fps = fps
        self.cursor_color = cursor_color
        self.dragging = False
        self.surface.fill((0, 0, 0, 0))
        self.text_surface = pygame.Surface((size[0] * 100, size[1])).convert_alpha()
        self.direct_status = [False, False]
        self.direct_timing = [0, 0]
        self.operating = False
        self.cursor_position = 0
        self.cursor_timing = 0
        self.cursor_position_px = 0
        self.lock = False
        self.backspace_timing = 0
        self.backspace_status = False
        self.del_status = False
        self.del_timing = 0
        self.text_surface_pos = 0
        self.character_pos = []
        self.selecting_pos = [-1, -1]
        self.selecting_pos_px = [-1, -1]
        self.last_clicked = False
        self.select_area_color = select_area_color
        self.do_color_reverse = do_color_reverse
        self.shift_status = False
        self.ctrl_status = False
        self.do_paste = False
        self.do_copy = False
        self.do_cut = False

    def set_as_background(self):
        self.background = self.surface.copy()

    def in_area(self, mouse_pos):
        return self.rect.collidepoint(*mouse_pos)

    def handel(self, event_r: pygame.event.Event):
        if self.operating:
            if event_r.type == pygame.TEXTINPUT and not self.ctrl_status:
                if self.selecting_pos[0] != self.selecting_pos[1]:
                    t_text = list(self.text)
                    for _ in range(abs(self.selecting_pos[0] - self.selecting_pos[1])):
                        try:
                            t_text.pop(min(self.selecting_pos))
                        except IndexError:
                            pass
                    self.text = ''.join(t_text)
                    self.cursor_position = min(self.selecting_pos)
                    self.selecting_pos = [-1, -1]
                t_text = list(self.text)
                t_text.insert(self.cursor_position, event_r.text)
                self.text = ''.join(t_text)
                self.cursor_position += len(event_r.text)
                self.cursor_timing = 0
            elif event_r.type == pygame.KEYDOWN:
                if event_r.key == pygame.K_BACKSPACE:
                    self.backspace_status = True
                elif event_r.key == pygame.K_LEFT:
                    self.direct_status[0] = True
                elif event_r.key == pygame.K_RIGHT:
                    self.direct_status[1] = True
                elif event_r.key == pygame.K_DELETE:
                    self.del_status = True
                elif event_r.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    self.ctrl_status = True
                    pygame.key.stop_text_input()
                if self.ctrl_status:
                    if event_r.key == pygame.K_c:
                        self.do_copy = True
                    elif event_r.key == pygame.K_v:
                        self.do_paste = True
                    elif event_r.key == pygame.K_x:
                        self.do_cut = True
                    elif event_r.key == pygame.K_a:
                        self.selecting_pos = [0, len(self.text)]
                        self.cursor_position = len(self.text)
            elif event_r.type == pygame.KEYUP:
                if event_r.key == pygame.K_BACKSPACE:
                    self.backspace_status = False
                elif event_r.key == pygame.K_LEFT:
                    self.direct_status[0] = False
                elif event_r.key == pygame.K_RIGHT:
                    self.direct_status[1] = False
                elif event_r.key == pygame.K_DELETE:
                    self.del_status = False
                elif event_r.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    self.ctrl_status = False
                    pygame.key.start_text_input()

        else:
            self.backspace_status = False
            self.direct_status[0] = False
            self.direct_status[1] = False
            self.del_status = False

    def operate(self, mouse_pos, mouse_press):
        if mouse_press[0] and not self.in_area(mouse_pos) and not self.dragging:
            self.lock = True
            self.operating = False
        if mouse_press[0] and self.in_area(mouse_pos) and not self.lock:
            self.operating = True
            pygame.key.set_text_input_rect((self.pos[0] + 5, self.pos[1] + (self.size[1] + self.font_size) // 2, 0, 0))
            pygame.key.start_text_input()
        if not mouse_press[0]:
            self.lock = False
            self.dragging = False
        if mouse_press[0]:
            self.dragging = True

        if self.backspace_status:
            self.cursor_timing = 0
            self.backspace_timing += 1
            if self.backspace_timing == 1 or (self.backspace_timing >= self.fps * 0.7 and self.backspace_timing % (self.fps // 25) == 0):
                if self.selecting_pos[0] == self.selecting_pos[1]:
                    if self.text != '' and self.cursor_position > 0:
                        t_text = list(self.text)
                        try:
                            t_text.pop(self.cursor_position - 1)
                        except IndexError:
                            pass
                        self.text = ''.join(t_text)
                        self.cursor_position -= 1
                else:
                    t_text = list(self.text)
                    for _ in range(abs(self.selecting_pos[0] - self.selecting_pos[1])):
                        try:
                            t_text.pop(min(self.selecting_pos))
                        except IndexError:
                            pass
                    self.text = ''.join(t_text)
                    self.cursor_position = min(self.selecting_pos)
                    self.selecting_pos = [-1, -1]
        else:
            self.backspace_timing = 0
        if self.del_status:
            self.cursor_timing = 0
            self.del_timing += 1
            if self.del_timing == 1 or (self.del_timing >= self.fps * 0.7 and self.del_timing % (self.fps // 25) == 0):
                if self.text != '' and self.cursor_position < len(self.text):
                    t_text = list(self.text)
                    try:
                        t_text.pop(self.cursor_position)
                    except IndexError:
                        pass
                    self.text = ''.join(t_text)
        else:
            self.del_timing = 0
        if self.direct_status[0]:
            self.selecting_pos = [-1, -1]
            self.cursor_timing = 0
            self.direct_timing[0] += 1
            if self.direct_timing[0] == 1 or (self.direct_timing[0] >= self.fps * 0.7 and self.direct_timing[0] % (self.fps // 15) == 0):
                self.cursor_position = max(self.cursor_position - 1, 0)
        else:
            self.direct_timing[0] = 0
        if self.direct_status[1]:
            self.selecting_pos = [-1, -1]
            self.cursor_timing = 0
            self.direct_timing[1] += 1
            if self.direct_timing[1] == 1 or (self.direct_timing[1] >= self.fps * 0.7 and self.direct_timing[1] % (self.fps // 15) == 0):
                self.cursor_position = min(self.cursor_position + 1, len(self.text))
        else:
            self.direct_timing[1] = 0

        if self.do_paste:
            if not pygame.scrap.get_init():
                pygame.scrap.init()
            clip_content = pygame.scrap.get(pygame.SCRAP_TEXT).decode(encoding='gb18030').strip('\x00')
            if self.selecting_pos[0] != self.selecting_pos[1]:
                t_text = list(self.text)
                for _ in range(abs(self.selecting_pos[0] - self.selecting_pos[1])):
                    try:
                        t_text.pop(min(self.selecting_pos))
                    except IndexError:
                        pass
                self.text = ''.join(t_text)
                self.cursor_position = min(self.selecting_pos)
                self.selecting_pos = [-1, -1]
            t_text = list(self.text)
            t_text.insert(self.cursor_position, clip_content)
            self.text = ''.join(t_text)
            self.cursor_position += len(clip_content)
            self.do_paste = False
        if self.do_copy:
            if self.selecting_pos[0] != self.selecting_pos[1]:
                if not pygame.scrap.get_init():
                    pygame.scrap.init()
                self.selecting_pos.sort()
                pygame.scrap.put(pygame.SCRAP_TEXT, self.text[self.selecting_pos[0]: self.selecting_pos[1]].encode(encoding='gb18030'))
                self.selecting_pos = [-1, -1]
            self.do_copy = False
        if self.do_cut:
            if self.selecting_pos[0] != self.selecting_pos[1]:
                if not pygame.scrap.get_init():
                    pygame.scrap.init()
                self.selecting_pos.sort()
                pygame.scrap.put(pygame.SCRAP_TEXT, self.text[self.selecting_pos[0]: self.selecting_pos[1]].encode(encoding='gb18030'))
                t_text = list(self.text)
                for _ in range(abs(self.selecting_pos[0] - self.selecting_pos[1])):
                    try:
                        t_text.pop(min(self.selecting_pos))
                    except IndexError:
                        pass
                self.text = ''.join(t_text)
                self.cursor_position = min(self.selecting_pos)
                self.selecting_pos = [-1, -1]

        self.do_cut = False

        self.surface.fill((0, 0, 0, 0))
        if self.background is not None:
            self.surface.blit(self.background, (0, 0))
        else:
            pygame.draw.rect(self.surface, self.background_color, (0, 0, *self.size), border_radius=self.border_radius)
        pos = 1
        cnt = 0
        min_delta = 2147483647
        cur_pos = -1
        self.character_pos.clear()
        self.cursor_position_px = pos - 1
        self.cursor_timing += 1
        self.text_surface.fill((0, 0, 0, 0))
        if self.text == '' and not self.operating:
            self.text_surface.blit(self.font_family.render(self.remind_text, 1, self.remind_text_color), (pos, (self.size[1] - self.font_size) // 2))

        for character in self.text:
            if cnt == self.cursor_position:
                self.cursor_position_px = pos - 1
            if self.operating:
                pygame.key.set_text_input_rect((self.pos[0] + pos + self.text_surface_pos, self.pos[1] + (self.size[1] + self.font_size) // 2, 0, 0))

            c_surface = self.font_family.render(character, 1, self.font_color)
            if min(self.selecting_pos) <= cnt < max(self.selecting_pos):
                if self.operating:
                    pygame.draw.rect(self.text_surface, self.select_area_color[0],
                                     (pos, (self.size[1] - self.font_size) // 2 - 2, c_surface.get_width(), self.font_size + 4))
                else:
                    pygame.draw.rect(self.text_surface, self.select_area_color[1],
                                     (pos, (self.size[1] - self.font_size) // 2 - 2, c_surface.get_width(), self.font_size + 4))
                if self.do_color_reverse and self.operating:
                    c_surface = self.font_family.render(character, 1, list(map(lambda x: 255 - x, self.font_color)))
            self.text_surface.blit(c_surface, (pos, (self.size[1] - self.font_size) // 2))
            self.character_pos.append(pos)
            if self.operating and mouse_press[0]:
                if min_delta > abs(pos - (mouse_pos[0] - self.pos[0] - 4 - self.text_surface_pos)):
                    min_delta = abs(pos - (mouse_pos[0] - self.pos[0] - 4 - self.text_surface_pos))
                    cur_pos = pos
                    self.cursor_position = cnt
            pos += c_surface.get_width()
            cnt += 1
            if self.operating and mouse_press[0]:
                if min_delta > abs(pos - (mouse_pos[0] - self.pos[0] - 4 - self.text_surface_pos)):
                    min_delta = abs(pos - (mouse_pos[0] - self.pos[0] - 4 - self.text_surface_pos))
                    cur_pos = pos
                    self.cursor_position = cnt

        if -self.text_surface_pos + self.size[0] - 10 > pos > self.size[0] - 4:
            self.text_surface_pos = self.size[0] - 10 - pos
        if pos < self.size[0] - 4:
            self.text_surface_pos = 0
        if cnt == self.cursor_position:
            self.cursor_position_px = pos - 1
        if mouse_press[0] and self.operating:
            self.cursor_position_px = cur_pos - 1
            self.cursor_timing = 0
        if self.operating and mouse_press[0]:
            if not self.last_clicked:
                self.selecting_pos = [self.cursor_position, self.cursor_position]
                self.selecting_pos_px = [self.cursor_position_px, self.cursor_position_px]
            else:
                self.selecting_pos[1] = self.cursor_position
                self.selecting_pos_px[1] = self.cursor_position_px

        if self.cursor_position_px < -self.text_surface_pos:
            self.text_surface_pos = -self.cursor_position_px
        if self.cursor_position_px > -self.text_surface_pos + self.size[0] - 10:
            self.text_surface_pos = -(self.cursor_position_px - self.size[0] + 10)
        if self.operating and (self.cursor_timing % (self.fps // 1) <= (self.fps // 2)):
            pygame.draw.rect(self.text_surface, self.cursor_color, (self.cursor_position_px, (self.size[1] - self.font_size) // 2, 2, self.font_size))

        self.surface.blit(self.text_surface, (self.text_surface_pos + 4, 0))
        self.last_clicked = mouse_press[0]

        if self.operating:
            item = 1
        else:
            item = 0
        pygame.draw.rect(self.surface, self.border_color[item], (0, 0, *self.size), border_radius=self.border_radius, width=self.border_width)
        self.screen.blit(self.surface, self.pos)


if __name__ == '__main__':
    screen = pygame.display.set_mode((800, 600))
    ib = InputBox((400, 31), (200, 200), screen, border_radius=5, border_width=3, remind_text='输入一些奇妙的东西')
    ib2 = InputBox((400, 31), (200, 300), screen, border_radius=5, border_width=3, remind_text='输入一些难绷的东西')
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ib.handel(event)
            ib2.handel(event)

        screen.fill((255, 255, 255))
        ib.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        ib2.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))

        if not ib.operating and not ib2.operating:
            pygame.key.stop_text_input()

        pygame.display.flip()
        clock.tick(60)
