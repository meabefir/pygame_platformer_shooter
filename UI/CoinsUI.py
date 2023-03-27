import pygame

import game_data
from Button import Button


class CoinsUI:
    def __init__(self):
        self.texture = pygame.transform.scale_by(pygame.image.load("assets/coin.png"), 3)
        self.texture.set_colorkey((255, 255, 255))

        self.text = Button(50, 0, 45, 45, (255, 255, 255), 32, '0', None, None, invisible_background=True)

        self.coins = 0

    def add_coin(self, amount=1):
        self.coins += amount
        self.text.text = str(self.coins)

    def render(self):
        self.text.draw(game_data.ui)
        game_data.ui.blit(self.texture, (0, 0))

