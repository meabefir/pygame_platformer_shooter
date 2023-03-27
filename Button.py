import copy

import pygame
from copy import deepcopy

class Button:
    def __init__(self, left, top, width, height, color, font_size, text, callback=None, params=None, font_color=(255, 255, 255), disabled=False, invisible_background=False, password=False):
        self.rect = pygame.Rect((left, top), (width, height))
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.font_size = font_size
        self.text = text
        self.callback = callback
        self.params = params
        self.disabled = disabled
        self.font_color = font_color
        self.invisible_background = invisible_background
        self.password = password

    def draw(self, screen):
        color = copy.deepcopy(self.color)
        inc = 0
        if self.is_mouse_over(pygame.mouse.get_pos()) and self.callback is not None:
            inc = -30
        if self.disabled:
            inc = -100
        color = (max(color[0] + inc, 0), max(color[1] + inc, 0), max(color[2] + inc, 0))
        if not self.invisible_background:
            pygame.draw.rect(screen, color, (self.left, self.top, self.width, self.height))

        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text if not self.password else "*" * len(self.text), True, self.font_color)
        text_rect = text.get_rect()
        text_rect.center = (self.left + self.width / 2, self.top + self.height / 2)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_mouse_over(pygame.mouse.get_pos()):
                    self.call()

    def update(self):
        pass

    def is_mouse_over(self, mouse_pos):
        x, y = mouse_pos
        return self.left <= x <= self.left + self.width and self.top <= y <= self.top + self.height

    def call(self):
        if self.callback is not None:
            self.callback(self.params)
