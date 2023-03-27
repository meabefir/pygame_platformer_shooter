import pygame

from Level import Level
from UI.PauseUI import PauseUI
from UI.LevelFinishUI import LevelFinishUI

class LevelScreen:
    def __init__(self, level):
        self.level = level

        self.paused = False
        self.finished = False
        self.pause_ui = PauseUI()
        self.finished_ui = None
        self.lost_ui = None

    def retry(self):
        self.level = Level(self.level.idx)
        self.paused = False
        self.finished = False
        self.finished_ui = None
        self.lost_ui = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause()

        if not self.paused:
            if self.finished:
                self.finished_ui.handle_event(event)
            elif self.lost_ui is not None:
                self.lost_ui.handle_event(event)
            else:
                self.level.handle_event(event)
        else:
            self.pause_ui.handle_event(event)


    def pause(self):
        self.paused = not self.paused

    def update(self, delta):
        if not self.paused and not self.finished and self.lost_ui is None:
            self.level.update(delta)
        else:
            pass

    def draw(self, screen):
        self.level.draw(screen)

        if self.paused:
            self.pause_ui.draw()
        elif self.finished:
            self.finished_ui.draw()
        elif self.lost_ui is not None:
            self.lost_ui.draw()