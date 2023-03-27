import pygame

import game_data

class Camera:
    def __init__(self, tracking=None):
        self.tracking = tracking
        self.rect = pygame.Rect(0, 0, game_data.WIDTH, game_data.HEIGHT)

    def track(self, obj):
        self.tracking = obj

    def update(self):
        if self.tracking is None:
            return
        self.rect.topleft = (
        self.tracking.rect.center[0] / game_data.render_scale, self.tracking.rect.center[1] / game_data.render_scale)

    def get_render_pos(self, pos):
        return (pos[0] - self.rect.x * game_data.render_scale + self.rect.width / 2 / game_data.render_scale, pos[1] - self.rect.y * game_data.render_scale + self.rect.height / 2 / game_data.render_scale)