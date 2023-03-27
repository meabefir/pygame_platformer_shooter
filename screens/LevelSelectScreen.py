import pygame

import game_data
from Button import Button
from Level import Level
from TextInput import TextInput

import database
from screens.LevelScreen import LevelScreen


class LevelSelectScreen:
    def __init__(self):
        self.background = pygame.Surface((game_data.WIDTH, game_data.HEIGHT))
        self.background.fill(game_data.COLOR1)

        self.title = Button(200, 100, 600, 100, game_data.COLOR2, 40, "Level selection", font_color=game_data.BLACK)
        self.level1 = Button(200, 300, 200, 65, game_data.COLOR2, 32, "Level 1", font_color=game_data.BLACK, callback=self.select_level, params=1)
        self.level2 = Button(200, 400, 200, 65, game_data.COLOR2, 32, "Level 2", font_color=game_data.BLACK, callback=self.select_level, params=2)
        self.level3 = Button(200, 500, 200, 65, game_data.COLOR2, 32, "Level 3", font_color=game_data.BLACK, callback=self.select_level, params=3)
        self.level4 = Button(600, 300, 200, 65, game_data.COLOR2, 32, "Level 4", font_color=game_data.BLACK, callback=self.select_level, params=4)
        self.level5 = Button(600, 400, 200, 65, game_data.COLOR2, 32, "Level 5", font_color=game_data.BLACK, callback=self.select_level, params=5)
        self.level6 = Button(600, 500, 200, 65, game_data.COLOR2, 32, "Level 6", font_color=game_data.BLACK, callback=self.select_level, params=6)

        self.back_button = Button(200, 600, 120, 65, game_data.COLOR2, 32, "Back", font_color=game_data.BLACK, callback=self.back)

    def back(self, p=None):
        from screens.MenuScreen import MenuScreen
        game_data.screen = MenuScreen()

    def select_level(self, level):
        print(level)
        game_data.screen = LevelScreen(Level(level))

    def handle_event(self, event):
        self.level1.handle_event(event)
        self.level2.handle_event(event)
        self.level3.handle_event(event)
        self.level4.handle_event(event)
        self.level5.handle_event(event)
        self.level6.handle_event(event)
        self.back_button.handle_event(event)

    def update(self, delta):
        pass

    def draw(self, screen):
        game_data.ui.blit(self.background, (0,0))

        self.title.draw(game_data.ui)
        self.level1.draw(game_data.ui)
        self.level2.draw(game_data.ui)
        self.level3.draw(game_data.ui)
        self.level4.draw(game_data.ui)
        self.level5.draw(game_data.ui)
        self.level6.draw(game_data.ui)
        self.back_button.draw(game_data.ui)