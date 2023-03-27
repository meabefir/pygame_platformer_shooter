import pygame
import os


class ImageTileScraper:
    def __init__(self, path, tile_size=None, offsets=None, scale=1):
        self.images = []
        self.scale = scale

        self.image = pygame.image.load(path)
        self.tile_size = tile_size
        if tile_size is None:
            self.tile_size = (self.image.get_height(), self.image.get_height())

            tiles_horizontal = self.image.get_width() // self.image.get_height()
            offsets = [(0, i) for i in range(tiles_horizontal)]
            print(offsets)

        for offset in offsets:
            offset = (offset[1], offset[0])
            cropped = pygame.Surface(self.tile_size)
            cropped.blit(self.image, (0, 0), (offset[0] * self.tile_size[0], offset[1] * self.tile_size[1], self.tile_size[0], self.tile_size[1]))

            scaled_image = pygame.transform.scale_by(cropped, self.scale)
            scaled_image.set_colorkey((0,0,0))
            self.images += [scaled_image]

    def get(self):
        return self.images
