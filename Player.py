import copy

import pygame

import database
import game_data
import globals
import sound

from AnimatedSprite import AnimatedSprite
from Camera import Camera
from PhysicsManager import PhysicsManager
from Timer import Timer
from UI.AmmoUI import AmmoUI
from UI.CoinsUI import CoinsUI
from Bullet import Bullet, BULLET_TYPE
from UI.LevelFinishUI import LevelFinishUI
from UI.LifeUI import LifeUI

from copy import deepcopy

from UI.LoseUI import LoseUI


class PLAYER_STATE:
    IDLE = 0
    RUN = 1
    USE = 2
    JUMP = 3
    HURT = 4
    DIE = 5

class WEAPON_STATE:
    SWORD = 0
    GUN = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, level, rect, lives):
        pygame.sprite.Sprite.__init__(self)

        self.level = level

        self.weapon = WEAPON_STATE.SWORD
        self.state = PLAYER_STATE.IDLE

        self.rect = pygame.Rect(rect.topleft, [18 * game_data.player_scale * 12.5, 25 * game_data.player_scale * 12.5])
        self.pos = [self.rect.center[0], self.rect.center[1]]
        self.original_pos = copy.deepcopy(self.pos)

        self.animations = {}
        self.load_animations()

        self.current_animation = self.animations[self.weapon][self.state]

        self._input = 0
        self.flip = True
        self.dir = 1
        self.velocity = [0, 0]
        self.speed = 330
        self.jump_force = 700
        self.on_ground = True
        self.should_jump = False

        self.dead = False

        self.coins_ui = CoinsUI()
        self.life_ui = LifeUI(self, lives)
        self.ammo_ui = AmmoUI()

        self.max_hp = 100
        self.current_hp = 100

        globals.main_camera = Camera(self)

        self.die_timer = None

        PhysicsManager.add_to_group("player", self)

    def load_animations(self):
        self.animations[WEAPON_STATE.SWORD] = {}
        self.animations[WEAPON_STATE.SWORD][PLAYER_STATE.IDLE] = AnimatedSprite(
            game_data.images["player"]["sword"]["idle"], .4, rect=self.rect, offset=(-2, -15))
        self.animations[WEAPON_STATE.SWORD][PLAYER_STATE.RUN] = AnimatedSprite(
            game_data.images["player"]["sword"]["run"], .4, rect=self.rect, offset=(-2, -20))
        self.animations[WEAPON_STATE.SWORD][PLAYER_STATE.USE] = AnimatedSprite(
            game_data.images["player"]["sword"]["use"], .3, False, rect=self.rect, execute_on_finish=[(self.use_finished, {})], offset=(-2, -20))
        self.animations[WEAPON_STATE.SWORD][PLAYER_STATE.JUMP] = AnimatedSprite(
            game_data.images["player"]["sword"]["jump"], .3, rect=self.rect)
        self.animations[WEAPON_STATE.SWORD][PLAYER_STATE.HURT] = AnimatedSprite(
            game_data.images["player"]["sword"]["hurt"], .3, rect=self.rect)

        self.animations[WEAPON_STATE.GUN] = {}
        self.animations[WEAPON_STATE.GUN][PLAYER_STATE.IDLE] = AnimatedSprite(game_data.images["player"]["gun"]["idle"],
                                                                              .4, rect=self.rect, offset=(-2, -15))
        self.animations[WEAPON_STATE.GUN][PLAYER_STATE.RUN] = AnimatedSprite(game_data.images["player"]["gun"]["run"],
                                                                             .4, rect=self.rect, offset=(-2, -20))
        self.animations[WEAPON_STATE.GUN][PLAYER_STATE.USE] = AnimatedSprite(game_data.images["player"]["gun"]["use"],
                                                                             .3, False, rect=self.rect, execute_on_finish=[(self.use_finished, {})], offset=(-2, -20))
        self.animations[WEAPON_STATE.GUN][PLAYER_STATE.JUMP] = AnimatedSprite(game_data.images["player"]["gun"]["jump"],
                                                                              .3, rect=self.rect)
        self.animations[WEAPON_STATE.GUN][PLAYER_STATE.HURT] = AnimatedSprite(game_data.images["player"]["gun"]["hurt"],
                                                                              .3, rect=self.rect)

        self.animations[WEAPON_STATE.SWORD][PLAYER_STATE.DIE] = AnimatedSprite(game_data.images["player"]["die"], 1, False, rect=self.rect, offset=(28, -28), execute_on_finish=[(self.respawn, {})])
        self.animations[WEAPON_STATE.GUN][PLAYER_STATE.DIE] = AnimatedSprite(game_data.images["player"]["die"], 1, False, rect=self.rect, offset=(28, -28), execute_on_finish=[(self.respawn, {})])

    def set_hp(self, hp, increase=False):
        self.current_hp = max(0, min(self.max_hp, hp))
        if self.current_hp == 0 and not increase:
            self.die()
        self.life_ui.set_percentage(self.current_hp / self.max_hp)

    def use_finished(self, p):
        if self._input != 0:
            self.set_state(PLAYER_STATE.RUN)
        else:
            self.set_state(PLAYER_STATE.IDLE)

    def change_weapon(self):
        if self.weapon == WEAPON_STATE.SWORD:
            self.set_weapon(WEAPON_STATE.GUN)
        else:
            self.set_weapon(WEAPON_STATE.SWORD)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == game_data.user["switch"]:
                self.change_weapon()
            elif event.key == game_data.user["use"]:
                self.set_state(PLAYER_STATE.USE)
            # elif event.key == pygame.K_t:
            #     self.die()
        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    def die(self):
        self.life_ui.lose_live()
        self.set_state(PLAYER_STATE.DIE)
        self._input = 0
        self.dead = True
        self.kill()

    def update_input(self):
        self._input = 0
        if pygame.key.get_pressed()[game_data.user["left"]]:
            self._input -= 1
            self.flip = True
        if pygame.key.get_pressed()[game_data.user["right"]]:
            self._input += 1
            self.flip = False
        if pygame.key.get_pressed()[game_data.user["jump"]] and self.on_ground:
            self.should_jump = True
        else:
            self.should_jump = False

        (leftclick, middleclick, rightclick) = pygame.mouse.get_pressed()
        if leftclick:
            self.set_state(PLAYER_STATE.USE)

    def update_animation(self):
        self.current_animation.reset()
        self.current_animation = self.animations[self.weapon][self.state]
        self.current_animation.reset()

    def set_state(self, new_state):
        if new_state == self.state:
            return
        self.state = new_state
        self.update_animation()

        if self.state == PLAYER_STATE.USE:
            self.use()
        elif self.state == PLAYER_STATE.DIE:
            pass

    def use(self):
        if self.weapon == WEAPON_STATE.GUN:
            if self.ammo_ui.ammo > 0:
                self.shoot()
        else:
            self.slash()

    def hit(self, damage):
        self.set_hp(self.current_hp - damage)

    def shoot(self):
        pass

        self.ammo_ui.use_ammo()
        bullet = Bullet(self.level, pygame.Rect(0, 0, 10, 10), (-1, 0) if self.flip else (1, 0), BULLET_TYPE.PLAYER)
        bullet.set_pos(self.rect.center)
        self.level.add_entity(bullet, 2)

    def slash(self):
        sound.play("slash", True)
        sprite = pygame.sprite.Sprite()
        rect = pygame.Rect(0,0,80,30)
        sprite.rect = rect
        if not self.flip:
            rect.center = self.rect.midright
        else:
            rect.center = self.rect.midleft
        for col in pygame.sprite.spritecollide(sprite, PhysicsManager.groups["enemy"], False):
            col.hit(50)
            sound.play("squish", True)

    def set_weapon(self, new_weapon):
        self.weapon = new_weapon
        self.update_animation()

    def pick_coins(self):
        collisions = self.get_collisions_with("coins")
        for coin in collisions:
            self.coin_picked(coin)

    def pick_hp(self):
        collisions = self.get_collisions_with("life")
        for life in collisions:
            self.current_hp += 40
            if self.current_hp >= self.max_hp:
                extra = self.current_hp - self.max_hp
                self.current_hp = extra
                self.life_ui.set_lives(self.life_ui.lives + 1)
            self.set_hp(self.current_hp, increase=True)
            life.remove(PhysicsManager.groups['life'])
            self.level.remove_entity(life)

    def pick_ammo(self):
        collisions = self.get_collisions_with("ammo")
        for a in collisions:
            self.ammo_ui.add_ammo(10)
            a.remove(PhysicsManager.groups['ammo'])
            self.level.remove_entity(a)

    def coin_picked(self, coin):
        coin.remove(PhysicsManager.groups['coins'])
        self.level.remove_entity(coin)
        self.collect_points(1)


    def collect_points(self, amount):
        self.coins_ui.add_coin(amount)

    def update(self, delta):
        self.pick_coins()
        self.pick_hp()
        self.pick_ammo()
        self.test_finish()
        if not self.dead:
            self.handle_danger()
        globals.main_camera.update()

        if self.state == PLAYER_STATE.IDLE:
            self.update_idle(delta)
        elif self.state == PLAYER_STATE.RUN:
            self.update_run(delta)
        elif self.state == PLAYER_STATE.USE:
            self.update_use(delta)
        elif self.state == PLAYER_STATE.JUMP:
            self.update_jump(delta)
        elif self.state == PLAYER_STATE.HURT:
            self.update_hurt(delta)
        elif self.state == PLAYER_STATE.DIE:
            self.update_die(delta)

        self.update_movement(delta)
        self.current_animation.update(delta)

    def draw(self, screen):
        if globals.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(globals.main_camera.get_render_pos(self.rect.topleft), self.rect.size))
            sprite = pygame.sprite.Sprite()
            rect = pygame.Rect(0, 0, 80, 30)
            sprite.rect = rect
            if not self.flip:
                rect.center = self.rect.midright
            else:
                rect.center = self.rect.midleft
            pygame.draw.rect(screen, (0, 255, 0),
                             pygame.Rect(globals.main_camera.get_render_pos(rect.topleft), rect.size))

        self.current_animation.draw(screen, self.flip)
        # self.current_animation.draw(screen, True)

        # slash debug

        self.coins_ui.render()
        self.life_ui.render()
        self.ammo_ui.render()

    def update_idle(self, delta):
        self.update_input()
        if self._input != 0:
            self.set_state(PLAYER_STATE.RUN)

    def update_run(self, delta):
        self.update_input()
        if self._input == 0:
            self.set_state(PLAYER_STATE.IDLE)

    def update_use(self, delta):
        self.update_input()

    def update_jump(self, delta):
        pass

    def update_hurt(self, delta):
        pass

    def update_die(self, delta):
        if self.die_timer:
            self.die_timer.update(delta)

    def get_collisions_with(self, group_name, any=False):
        return pygame.sprite.spritecollide(self, PhysicsManager.groups[group_name], False) if not any else pygame.sprite.spritecollideany(self, PhysicsManager.groups[group_name])

    def update_movement(self, delta):
        self.velocity[0] = self._input * self.speed * delta
        self.velocity[1] += game_data.G * delta
        self.velocity[1] = min(self.velocity[1], game_data.MAX_VERTICAL_VELOCITY)

        if self.should_jump:
            self.velocity[1] = -self.jump_force * delta
            self.on_ground = False

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

    def handle_danger(self):
        collisions = self.get_collisions_with("danger")
        if len(collisions):
            self.die()

    def respawn(self, p=None):
        self.pos = copy.deepcopy(self.original_pos)
        self.rect.center = (self.original_pos[0], self.original_pos[1])
        self.dead = False
        self.set_state(PLAYER_STATE.IDLE)
        PhysicsManager.add_to_group("player", self)
        self.set_hp(self.max_hp)

        if self.life_ui.lives == 0:
            self.lose()

    def lose(self):
        game_data.screen.lost_ui = LoseUI()

    def test_finish(self):
        collisions = self.get_collisions_with("flag")
        if len(collisions):
            self.end_level()

    def end_level(self):
        game_data.screen.finished = True

        prev_points = game_data.user[f"points{self.level.idx}"]
        points = self.coins_ui.coins
        game_data.screen.finished_ui = LevelFinishUI(prev_points, points)

        if points > prev_points:
            database.update_points(game_data.user["username"], f"points{self.level.idx}", points)
            game_data.user[f"points{self.level.idx}"] = points
