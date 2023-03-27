import pygame
import os


class ImageScraper:
    def __init__(self, path, scale):
        self.images = []
        self.scale = scale
        for d, sd, files in os.walk(path):
            for f in files:
                scaled_image = pygame.transform.scale_by(pygame.image.load(f'{d}/{f}'), self.scale)
                self.images += [scaled_image]

    def get(self):
        return self.images
