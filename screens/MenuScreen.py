import pygame

import game_data
import sound
from Button import Button
from TextInput import TextInput

import database
from screens.LeaderboardScreen import LeaderboardScreen
from screens.LevelSelectScreen import LevelSelectScreen
from screens.SettingsScreen import SettingsScreen


class MenuScreen:
    def __init__(self):
        self.background = pygame.Surface((game_data.WIDTH, game_data.HEIGHT))
        self.background.fill(game_data.COLOR1)

        self.title = Button(200, 100, 600, 100, game_data.COLOR2, 40, game_data.user["username"], font_color=game_data.BLACK)
        self.play_button = Button(200, 300, 200, 65, game_data.COLOR2, 32, "Play", font_color=game_data.BLACK, callback=self.play, params=None)
        self.settings_button = Button(200, 400, 200, 65, game_data.COLOR2, 32, "Settings", font_color=game_data.BLACK, callback=self.settings, params=None)
        self.leaderboard_button = Button(200, 500, 200, 65, game_data.COLOR2, 32, "Leaderboard", font_color=game_data.BLACK, callback=self.leaderboard, params=None)

        sound.stop("jungle")
        sound.play("menu")

    def play(self, p):
        game_data.screen = LevelSelectScreen()

    def settings(self, p):
        game_data.screen = SettingsScreen()

    def leaderboard(self, p):
        game_data.screen = LeaderboardScreen()

    def handle_event(self, event):
        self.play_button.handle_event(event)
        self.settings_button.handle_event(event)
        self.leaderboard_button.handle_event(event)

    def update(self, delta):
        pass

    def draw(self, screen):
        game_data.ui.blit(self.background, (0,0))

        self.title.draw(game_data.ui)
        self.play_button.draw(game_data.ui)
        self.settings_button.draw(game_data.ui)
        self.leaderboard_button.draw(game_data.ui)