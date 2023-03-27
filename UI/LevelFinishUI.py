import pygame

import game_data
from Button import Button

class LevelFinishUI:
    def __init__(self, prev_points=0, points=0):
        self.offset = (300, 300)
        self.background = pygame.Surface((game_data.WIDTH - self.offset[0], game_data.HEIGHT - self.offset[1]))
        self.background.fill(game_data.COLOR1)

        self.info1 = Button(350 + self.offset[0]/2, 50 + self.offset[1]/2, 300, 30, game_data.WHITE, 30, "Level Completed!", disabled=True, invisible_background=True, font_color=game_data.BLACK)
        message = f"Good job! You got a new personal best of {points} points" if points > prev_points else f"You collected {points} points! Try and collect even more!"
        self.info2 = Button(game_data.WIDTH/2 - 700/2, 150 + self.offset[1]/2, 700, 60, game_data.WHITE, 30, message, disabled=True, invisible_background=True, font_color=game_data.BLACK)

        w = 200
        self.menu_button = Button(game_data.WIDTH / 2 - w / 2 - 150, 250 + self.offset[1] / 2, w, 30,
                                  game_data.COLOR2, 30, "Menu", font_color=game_data.BLACK, callback=self.menu,
                                  params=None)
        self.play_again = Button(game_data.WIDTH / 2 - w / 2 + 150, 250 + self.offset[1] / 2, w, 30,
                                 game_data.COLOR2, 30, "Retry", font_color=game_data.BLACK, callback=self.retry,
                                 params=None)

    def menu(self, p=None):
            from screens.MenuScreen import MenuScreen
            game_data.screen = MenuScreen()

    def retry(self, p):
        game_data.screen.retry()

    def handle_event(self, event):
        self.menu_button.handle_event(event)
        self.play_again.handle_event(event)

    def update(self, delta):
        pass

    def draw(self):
        game_data.ui.blit(self.background, (self.offset[0]/2, self.offset[1]/2))

        self.info1.draw(game_data.ui)
        self.info2.draw(game_data.ui)
        self.menu_button.draw(game_data.ui)
        self.play_again.draw(game_data.ui)

