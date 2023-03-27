import pygame

import game_data
from Button import Button


class LifeUI:
    def __init__(self, player, lives):
        self.player = player
        self.texture = pygame.transform.scale_by(pygame.image.load("assets/life.png"), 1.5)
        self.texture.set_colorkey((255, 255, 255))

        self.lives = lives
        self.percentage = 1

        self.height = 40
        self.width = 200

    def lose_live(self):
        self.set_lives(self.lives - 1)

    def set_lives(self, value):
        self.lives = value

    def set_percentage(self, value):
        self.percentage = value

    def render(self):
        for i in range(self.lives):
            game_data.ui.blit(self.texture, (game_data.WIDTH - (i+1)*self.texture.get_width(), 0))

        # bar
        pygame.draw.rect(game_data.ui, (255, 0, 0), pygame.Rect(game_data.WIDTH - self.width - 10, self.texture.get_height() + 5, self.width, self.height))
        pygame.draw.rect(game_data.ui, (0, 255, 0), pygame.Rect(game_data.WIDTH - self.width - 10, self.texture.get_height() + 5, self.percentage * self.width, self.height))