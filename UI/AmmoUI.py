import pygame

import game_data
from Button import Button


class AmmoUI:
    def __init__(self):
        self.texture = pygame.transform.scale_by(pygame.image.load("assets/ammo_box.png"), 1.5)
        self.texture.set_colorkey((255, 255, 255))

        self.text = Button(50, 50, 45, 45, (255, 255, 255), 32, '5', None, None, invisible_background=True)

        self.ammo = 5

    def add_ammo(self, count):
        self.ammo += count
        self.text.text = str(self.ammo)

    def use_ammo(self):
        self.ammo -= 1
        self.text.text = str(self.ammo)

    def render(self):
        self.text.draw(game_data.ui)
        game_data.ui.blit(self.texture, (0, 50))

