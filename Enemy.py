import pygame

import globals
import game_data
from AnimatedSprite import AnimatedSprite
from Bullet import Bullet, BULLET_TYPE
from PhysicsManager import PhysicsManager
from Timer import Timer


class ENEMY_TYPE:
    GIRL = 1
    ROBOT = 2
    GUNNER = 3

class ENEMY_STATE:
    RUN = 0
    SHOOT = 1
    DIE = 2

data = {
    ENEMY_TYPE.GIRL: {
        "speed": 220,
        "hp": 100,
        "vision": 350,
        "bullet_type": BULLET_TYPE.ENEMY,
        "shoot_delay": .3,
        "points": 2
    },
    ENEMY_TYPE.ROBOT: {
        "speed": 120,
        "hp": 300,
        "vision": 250,
        "bullet_type": BULLET_TYPE.ENEMY2,
        "shoot_delay": 1.5,
        "points": 5
    },
    ENEMY_TYPE.GUNNER: {
        "speed": 180,
        "hp": 200,
        "vision": 250,
        "bullet_type": BULLET_TYPE.ENEMY3,
        "shoot_delay": .2,
        "points": 3
    },
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, rect, _type=ENEMY_TYPE.GIRL):
        pygame.sprite.Sprite.__init__(self)

        self.level = level
        self._input = 1
        self.velocity = [0, 0]
        self.pos = [rect.x, rect.y]

        self.speed = data[_type]["speed"]
        self.hp = data[_type]["hp"]
        self.bullet_type = data[_type]["bullet_type"]
        self.shoot_delay = data[_type]["shoot_delay"]
        self.points = data[_type]["points"]

        self.can_shoot = True
        self.shoot_timer = Timer(self.shoot_delay, [(self.set_can_shoot, True)], auto_restart=True)

        self.rect = rect
        self._type = _type

        self.animations = {}
        self.current_animation = None

        self.load_animations()

        self.state = None
        self.set_state(ENEMY_STATE.RUN)

        self.flip = False
        self.on_ground = True

        self.left_rect = pygame.Rect(0,0,10,10)
        self.right_rect = pygame.Rect(0,0,10,10)
        self.vision_rect = pygame.Rect(0,0,data[_type]["vision"],10)

        PhysicsManager.add_to_group("enemy", self)

    def set_can_shoot(self, val):
        self.can_shoot = val

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        self.set_state(ENEMY_STATE.DIE)
        self.kill()
        self.level.get_player().collect_points(self.points)

    def set_state(self, state):
        if state == self.state:
            return
        self.state = state
        self.update_animation()

        if self.state == ENEMY_STATE.SHOOT:
            self.shoot()

    def update_animation(self):
        if self.current_animation:
            self.current_animation.reset()
        self.current_animation = self.animations[self.state]
        self.current_animation.reset()

    def load_animations(self):
        self.animations[ENEMY_STATE.RUN] = AnimatedSprite(
            game_data.images["enemy"][self._type]["run"], .6, rect=self.rect)
        self.animations[ENEMY_STATE.SHOOT] = AnimatedSprite(
            game_data.images["enemy"][self._type]["shoot"], .4, False, rect=self.rect, execute_on_finish=[(self.shoot_finish, None)])
        self.animations[ENEMY_STATE.DIE] = AnimatedSprite(
            game_data.images["enemy"][self._type]["die"], .4, False, rect=self.rect, execute_on_finish=[(self.die_finish, None)])

    def shoot_finish(self, p=None):
        self.set_state(ENEMY_STATE.RUN)

    def die_finish(self, p):
        self.level.remove_entity(self)
        self.kill()

    def handle_event(self, e):
        pass

    def get_collisions_with(self, group_name, any=False):
        return pygame.sprite.spritecollide(self, PhysicsManager.groups[group_name], False) if not any else pygame.sprite.spritecollideany(self, PhysicsManager.groups[group_name])


    def update_movement(self, delta):
        self.velocity[0] = self._input * self.speed * delta
        self.velocity[1] += game_data.G * delta
        self.velocity[1] = min(self.velocity[1], game_data.MAX_VERTICAL_VELOCITY)

        # if self.should_jump:
        #     self.velocity[1] -= self.jump_force
        #     self.on_ground = False

        self.pos[0] += self.velocity[0]
        self.rect.center = (self.pos[0], self.pos[1])

        # check if we hit something on the x axis
        col = self.get_collisions_with("static", True)
        if col is not None:
            # check if colliding below
            if col.rect.left < self.rect.right and self.rect.left < col.rect.left:
                self.pos[0] -= self.rect.right - col.rect.left
                self.rect.center = self.pos
            elif col.rect.right > self.rect.left and col.rect.right < self.rect.right:
                self.pos[0] += col.rect.right - self.rect.left
                self.rect.center = self.pos

            self._input *= -1
            self.flip = not self.flip

        self.pos[1] += self.velocity[1]
        self.rect.center = (self.pos[0], self.pos[1])

        # check if we hit something on the y axis
        col = self.get_collisions_with("static", True)
        if col is not None:
            # check if colliding below
            if col.rect.top < self.rect.bottom and self.rect.top < col.rect.top:
                self.pos[1] -= self.rect.bottom - col.rect.top
                self.rect.center = self.pos
                self.on_ground = True
            elif col.rect.bottom > self.rect.top and col.rect.bottom < self.rect.bottom:
                self.pos[1] += col.rect.bottom - self.rect.top
                self.rect.center = self.pos
                self.velocity[1] = 0
        else:
            self.on_ground = False

        # check left and right rects
        left_sprite = pygame.sprite.Sprite()
        left_sprite.rect = self.left_rect
        if not pygame.sprite.spritecollideany(left_sprite, PhysicsManager.groups["static"]):
            self._input = 1
            self.flip = False
        right_sprite = pygame.sprite.Sprite()
        right_sprite.rect = self.right_rect
        if not pygame.sprite.spritecollideany(right_sprite, PhysicsManager.groups["static"]):
            self._input = -1
            self.flip = True

        self.update_rects()

    def update(self, delta):
        self.current_animation.update(delta)
        self.shoot_timer.update(delta)

        if self.state == ENEMY_STATE.RUN:
            self.update_run(delta)
        elif self.state == ENEMY_STATE.SHOOT:
            self.update_shoot(delta)
        elif self.state == ENEMY_STATE.DIE:
            self.update_die(delta)

    def update_run(self, delta):
        self.update_movement(delta)

        # check for player
        sprite = pygame.sprite.Sprite()
        sprite.rect = self.vision_rect
        if pygame.sprite.spritecollideany(sprite, PhysicsManager.groups["player"]) and self.can_shoot:
            self.set_state(ENEMY_STATE.SHOOT)

    def shoot(self):
        bullet = Bullet(self.level, pygame.Rect(0, 0, 10, 10), (-1, 0) if self.flip else (1, 0), self.bullet_type)
        bullet.set_pos(self.rect.center)
        self.level.add_entity(bullet, 2)
        self.can_shoot = False

    def update_shoot(self, delta):
        pass

    def update_die(self, delta):
        pass

    def draw(self, screen):
        # debug
        if globals.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.Rect(globals.main_camera.get_render_pos(self.rect.topleft), self.rect.size))
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.Rect(globals.main_camera.get_render_pos(self.left_rect.topleft), self.left_rect.size))
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.Rect(globals.main_camera.get_render_pos(self.right_rect.topleft), self.right_rect.size))
            pygame.draw.rect(screen, (0, 255, 0),
                             pygame.Rect(globals.main_camera.get_render_pos(self.vision_rect.topleft), self.vision_rect.size))

        self.current_animation.draw(screen, self.flip)

    def update_rects(self):
        self.left_rect.topright = self.rect.bottomleft
        self.right_rect.topleft = self.rect.bottomright

        self.vision_rect.center = self.rect.center
        offset = 30
        if not self.flip:
            self.vision_rect.left = self.rect.left + offset
        else:
            self.vision_rect.right = self.rect.right - offset
