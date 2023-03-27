import pygame

import game_data
from Button import Button
from Timer import Timer


class TextInput:
    def __init__(self, left, top, width, height, color, font_size, password=False, font_color=(0,0,0), text=""):
        self.rect = pygame.Rect(left, top, width, height)
        self.text = Button(left, top, width, height, color, font_size, text, None, {}, password=password, font_color=font_color)
        self.current_text = text
        self.active = True
        self.can_delete = True

    def set_can_delete(self, p=None):
        self.can_delete = True

    def handle_event(self, event):
        self.text.handle_event(event)
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == 8:
                if len(self.current_text) > 0:
                    self.current_text = self.current_text[:-1]

                    self.text.text = self.current_text

            if (pygame.K_a <= event.key <= pygame.K_z or pygame.K_0 <= event.key <= pygame.K_9) and len(self.current_text) < 20:
                self.current_text += chr(event.key)

                self.text.text = self.current_text

    def draw(self, surface):
        self.text.draw(surface)