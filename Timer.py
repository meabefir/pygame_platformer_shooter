import pygame


class Timer:
    def __init__(self, time, actions, active=True, auto_restart=False):
        self.time = time
        self.current_time = 0
        self.actions = actions
        self.active = active
        self.auto_restart = auto_restart
        self.shot = False

    def reset(self):
        self.shot = False

    def update(self, delta):
        if not self.active:
            return

        self.current_time += delta

        if self.current_time >= self.time:
            if self.auto_restart:
                self.current_time -= self.time
            elif self.shot:
                return
            for (f, p) in self.actions:
                f(p)
            self.shot = True
