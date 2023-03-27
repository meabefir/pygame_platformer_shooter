import pygame
import json

import game_data
import sound
from AnimatedSprite import AnimatedSprite
from Enemy import Enemy, ENEMY_TYPE
from PhysicsManager import PhysicsManager
from Player import Player


class Tile(pygame.sprite.Sprite):
    def __init__(self, animated_sprite, group):
        self.group = group
        pygame.sprite.Sprite.__init__(self)

        self.animated_sprite = animated_sprite
        self.rect = self.animated_sprite.rect

        PhysicsManager.add_to_group(group, self)

    def handle_event(self, e):
        pass

    def update(self, delta):
        self.animated_sprite.update(delta)

    def draw(self, screen):
        self.animated_sprite.draw(screen)
        # pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Level:
    def __init__(self, idx=1):
        PhysicsManager.reset()
        self.idx = idx
        self.tiles = []

        with open(f"assets/level_data/level{idx}.json") as json_file:
            self.data = json.load(json_file)

        self.type = self.data["type"]
        self.entities = []

        self.load_tiles()

        sound.stop("menu")
        sound.play("jungle")

    def load_tiles(self):
        for ir, row in enumerate(self.data["tiles"]):
            for ic, t in enumerate(row):
                if t == '.':
                    continue

                image = game_data.images[self.type][t] if t not in game_data.invalid_tiles else None
                entity = None

                rect = pygame.Rect(ic * game_data.TILE_SIZE, ir * game_data.TILE_SIZE, game_data.TILE_SIZE, game_data.TILE_SIZE)
                render_order = 0

                if t in game_data.wall_tiles:
                    entity = Tile(AnimatedSprite(image, -1, False, rect), 'static')
                elif t == '$':
                    entity = Tile(AnimatedSprite(image, .5, True, rect), 'coins')
                elif t == 'H':
                    entity = Tile(AnimatedSprite(image, -1, True, rect), 'life')
                elif t == '^':
                    entity = Tile(AnimatedSprite(image, -1, True, rect), 'ammo')
                elif t == 'F':
                    entity = Tile(AnimatedSprite(image, -1, True, rect), 'flag')
                elif t == '/':
                    entity = Tile(AnimatedSprite(image, .6, True, rect), 'danger')
                elif t == 'x':
                    entity = Tile(AnimatedSprite(image, -1, True, rect), 'danger')
                elif t == '@':
                    entity = Player(self, rect, self.data["lives"])
                    render_order = 1
                elif t == '1':
                    rect = pygame.Rect(ic * game_data.TILE_SIZE, ir * game_data.TILE_SIZE, 22 * game_data.enemy_scale * 12.5, 40 * game_data.enemy_scale * 12.5)
                    rect.bottomright = (ic * game_data.TILE_SIZE, (ir+1) * game_data.TILE_SIZE)
                    entity = Enemy(self, rect, ENEMY_TYPE.GIRL)
                    render_order = 1
                elif t == '2':
                    rect = pygame.Rect(ic * game_data.TILE_SIZE, ir * game_data.TILE_SIZE, 22 * game_data.enemy_scale * 12.5, 40 * game_data.enemy_scale * 12.5)
                    rect.bottomright = (ic * game_data.TILE_SIZE, (ir+1) * game_data.TILE_SIZE)
                    entity = Enemy(self, rect, ENEMY_TYPE.ROBOT)
                    render_order = 1
                elif t == '3':
                    rect = pygame.Rect(ic * game_data.TILE_SIZE, ir * game_data.TILE_SIZE, 22 * game_data.enemy_scale * 12.5, 40 * game_data.enemy_scale * 12.5)
                    rect.bottomright = (ic * game_data.TILE_SIZE, (ir+1) * game_data.TILE_SIZE)
                    entity = Enemy(self, rect, ENEMY_TYPE.GUNNER)
                    render_order = 1


                if entity is None:
                    continue
                entity.render_order = render_order
                self.entities += [entity]
        self.entities.sort(key=lambda e: e.render_order)

    def remove_entity(self, tile):
        try:
            self.entities.remove(tile)
        except:
            pass

    def handle_event(self, event):
        for e in self.entities:
            e.handle_event(event)

    def update(self, delta):
        for e in self.entities:
            e.update(delta)

    def draw(self, screen):
        surface = pygame.Surface((game_data.WIDTH,game_data.HEIGHT))
        surface.fill((50, 200, 0))
        surface.set_alpha(55)
        screen.blit(surface, (0,0))
        for e in self.entities:
            e.draw(screen)

    def add_entity(self, e, order):
        e.render_order = order
        self.entities += [e]
        self.entities.sort(key= lambda e: e.render_order)

    def get_player(self):
        for en in self.entities:
            if isinstance(en, Player):
                return en
        return None