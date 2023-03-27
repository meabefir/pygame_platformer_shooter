import pygame


class PhysicsManager:
    groups = {}

    @classmethod
    def init(cls):
        cls.groups = {

        }

        x = pygame.sprite.Group()

    @classmethod
    def add_to_group(cls, group, sprite):
        if group not in cls.groups.keys():
            cls.groups[group] = pygame.sprite.Group()
        cls.groups[group].add(sprite)

    @classmethod
    def reset(cls):
        for key, val in cls.groups.items():
            val.empty()