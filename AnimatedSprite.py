import pygame
import os
import globals

class AnimatedSprite:
    def __init__(self, images, speed=-1, loop=True, rect=None, execute_on_finish=None, offset=(0, 0)):
        if execute_on_finish is None:
            execute_on_finish = []
        if rect is None:
            rect = pygame.Rect(0, 0, 0, 0)
        self.speed = speed
        self.rect = rect
        self.loop = loop
        self.frames = []
        self.current_frame = 0
        self.offset = offset

        self.frames = images

        self.frame_duration = speed / max(len(self.frames), 1)
        self.current_time = 0
        self.execute_on_finish = execute_on_finish

    def reset(self):
        self.current_frame = 0
        self.current_time = 0

    def handle_event(self, event):
        pass

    def reset(self):
        self.current_frame = 0
        self.current_time = 0

    def update(self, delta):
        if self.speed <= 0:
            return
        self.current_time += delta
        if self.current_time >= self.frame_duration:
            self.current_time -= self.frame_duration
            # self.current_frame = (self.current_frame + 1) % len(self.frames) if self.loop else min(
            #     self.current_frame + 1, len(self.frames) - 1)
            # self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.current_frame = (self.current_frame + 1)

            if self.loop:
                self.current_frame %= len(self.frames)
                if self.current_frame == 0:
                    for (f, p) in self.execute_on_finish:
                        f(p)
            else:
                if self.current_frame == len(self.frames):
                    for (f, p) in self.execute_on_finish:
                        f(p)

            # if self.current_frame == 0 and not self.loop:
            #     for (f, p) in self.execute_on_finish:
            #         f(p)

    def draw(self, screen, flip=False):
        # screen.blit(pygame.transform.flip(self.frames[self.current_frame], flip, False), (self.rect.topleft[0] - (offset[0] if flip else 0), self.rect.topleft[1] - (offset[1] if flip else 0)))
        # texture size offset
        pos = (self.rect.midtop[0] - self.frames[0].get_width()/2 - (self.offset[0] if not flip else -self.offset[0]), self.rect.midtop[1] + self.offset[1])
        # camera offset
        pos = globals.main_camera.get_render_pos(pos)

        screen.blit(pygame.transform.flip(self.frames[min(self.current_frame, len(self.frames)-1)], flip, False), pos)
