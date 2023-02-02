# импорт библиотек
from text import TextObject
from config import *
from pygame.rect import Rect


class Button:
    # инициализация
    def __init__(self, x, y, w, h, text, on_click=lambda x: None, padding=0):
        self.bounds = Rect(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click

        self.text = TextObject(x + padding, y + padding - 10, lambda: text, BUTTON_TEXT_COLOR, FONT_NAME, FONT_SIZE)

    @property
    def back_color(self):
        return dict(normal=BUTTON_NORMAL_COLOR,
                    hover=BUTTON_HOVER_COLOR,
                    pressed=BUTTON_PRESS_COLOR)[self.state]

    # отрисовка кнопок
    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.bounds)
        self.text.draw(surface)

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'
