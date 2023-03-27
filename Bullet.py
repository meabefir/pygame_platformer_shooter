import pygame

import globals
import sound
from AnimatedSprite import AnimatedSprite
from ImageScraper import ImageScraper
from PhysicsManager import PhysicsManager
from Timer import Timer


class BULLET_TYPE:
    PLAYER = 0
    ENEMY = 1
    ENEMY2 = 2
    ENEMY3 = 3

data = {
    BULLET_TYPE.PLAYER: {
        "image": pygame.image.load("assets/bullet.png"),
        "damage": 90,
        "target": "enemy",
        "speed": 1350,
        "sound": "player_shoot"
    },
    BULLET_TYPE.ENEMY: {
        "image": pygame.image.load("assets/bullet.png"),
        "damage": 10,
        "target": "player",
        "speed": 150,
        "sound": "9mm"
    },
    BULLET_TYPE.ENEMY2: {
        "image": pygame.transform.scale_by(pygame.image.load("assets/bullet2.png"), .15),
        "damage": 30,
        "target": "player",
        "speed": 100,
        "sound": "fireball"
    },
    BULLET_TYPE.ENEMY3: {
        "image":  pygame.image.load("assets/bullet.png"),
        "damage": 10,
        "target": "player",
        "speed": 500,
        "sound": "9mm"
    },
}

class Bullet(pygame.sprite.Sprite):
    def __init__(self, level, rect, _dir, type):
        pygame.sprite.Sprite.__init__(self)

        self.type = type
        self.level = level
        self.rect = rect
        self._dir = _dir
        self.image = data[type]["image"] if _dir[0] == 1 else pygame.transform.flip(data[type]["image"], True, False)
        self.damage = data[type]["damage"]
        self.target = data[type]["target"]
        self.speed = data[type]["speed"]
        self.pos = rect.topleft

        self.timer = Timer(1, [(self.destroy, {})])

        sound.play(data[type]["sound"], True)

    def destroy(self, p=None):
        self.kill()
        self.level.remove_entity(self)

    def set_pos(self, pos):
        self.rect.center = pos
        self.pos = pos

    def handle_event(self, e):
        pass

    def update(self, delta):
        self.pos = (self.pos[0] + self._dir[0] * self.speed * delta, self.pos[1] + self._dir[1] * self.speed * delta)
        self.rect.center = self.pos

        self.timer.update(delta)
        # colision detection
        for col in pygame.sprite.spritecollide(self, PhysicsManager.groups[self.target], False):
            col.hit(self.damage)
            self.destroy()

    def draw(self, screen):
        if globals.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.Rect(globals.main_camera.get_render_pos(self.rect.topleft), self.rect.size))

        pos = (self.rect.center[0] - self.image.get_width()/2, self.rect.center[1] - self.image.get_height()/2)

        screen.blit(self.image, globals.main_camera.get_render_pos(pos))