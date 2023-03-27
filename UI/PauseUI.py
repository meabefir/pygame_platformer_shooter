import pygame

import game_data
from Button import Button

class PauseUI:
    def __init__(self):
        self.offset = (300, 300)
        self.background = pygame.Surface((game_data.WIDTH - self.offset[0], game_data.HEIGHT - self.offset[1]))
        self.background.fill(game_data.COLOR1)

        self.info1 = Button(350 + self.offset[0]/2, 50 + self.offset[1]/2, 300, 30, game_data.WHITE, 30, "Press escape to unpause", disabled=True, invisible_background=True, font_color=game_data.BLACK)

        self.menu_button = Button(150 + self.offset[0]/2, 250 + self.offset[1]/2, 300, 30, game_data.COLOR2, 30, "Menu", font_color=game_data.BLACK, callback=self.menu, params=None)
        self.settings_button = Button(550 + self.offset[0]/2, 250 + self.offset[1]/2, 300, 30, game_data.COLOR2, 30, "Settings", font_color=game_data.BLACK, callback=self.settings, params=None)

    def menu(self, p=None):
        from screens.MenuScreen import MenuScreen
        game_data.screen = MenuScreen()

    def settings(self, p=None):
        from screens.SettingsScreen import SettingsScreen
        game_data.screen = SettingsScreen(game_data.screen)

    def handle_event(self, event):
        self.menu_button.handle_event(event)
        self.settings_button.handle_event(event)

    def update(self, delta):
        pass

    def draw(self):
        game_data.ui.blit(self.background, (self.offset[0]/2, self.offset[1]/2))

        self.info1.draw(game_data.ui)
        self.menu_button.draw(game_data.ui)
        self.settings_button.draw(game_data.ui)

