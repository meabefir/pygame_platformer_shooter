import pygame

import game_data
import sound
from Button import Button
from TextInput import TextInput

import database
from screens.MenuScreen import MenuScreen


class LoginScreen:
    def __init__(self):
        self.background = pygame.Surface((game_data.WIDTH, game_data.HEIGHT))
        self.background.fill(game_data.COLOR1)

        self.title = Button(200, 100, 600, 100, game_data.COLOR2, 40, "SAVE THE JUNGLE", font_color=game_data.BLACK)
        self.login_button = Button(200, 300, 200, 65, game_data.COLOR2, 32, "Login", font_color=game_data.BLACK, callback=self.login, params=None)
        self.register_button = Button(200, 400, 200, 65, game_data.COLOR2, 32, "Register", font_color=game_data.BLACK, callback=self.register, params=None)

        self.username_input = TextInput(600, 300, 300, 65, game_data.COLOR2, 28, False, text="user2")
        self.username_input.text.callback = self.set_active
        self.username_input.text.params = self.username_input

        self.password_input = TextInput(600, 400, 300, 65, game_data.COLOR2, 28, True, text="password2")
        self.password_input.active = False
        self.password_input.text.callback = self.set_active
        self.password_input.text.params = self.password_input

        self.error = Button(200, 600, 600, 65, game_data.COLOR2, 28, "", font_color=game_data.RED, invisible_background=True)

        sound.play("menu")

    def set_active(self, input):
        if input == self.username_input:
            self.username_input.active = True
            self.password_input.active = False
        else:
            self.username_input.active = False
            self.password_input.active = True

    def login(self, p=None):
        if not self.validate_input():
            return
        ret = database.login_user(self.username_input.text.text, self.password_input.text.text)
        if ret is None:
            self.error.text = "Login failed"
        else:
            print("login succesfull, switch to main menu")
            game_data.user = ret
            game_data.screen = MenuScreen()

    def register(self, p):
        if not self.validate_input():
            return
        ret = database.create_user(self.username_input.text.text, self.password_input.text.text)
        if ret is False:
            self.error.text = 'User already exists'
            return
        self.login()

    def handle_event(self, event):
        self.login_button.handle_event(event)
        self.register_button.handle_event(event)
        self.error.handle_event(event)

        self.username_input.handle_event(event)
        self.password_input.handle_event(event)

    def update(self, delta):
        pass

    def draw(self, screen):
        game_data.ui.blit(self.background, (0,0))

        self.title.draw(game_data.ui)
        self.error.draw(game_data.ui)
        self.login_button.draw(game_data.ui)
        self.register_button.draw(game_data.ui)

        border = 5
        if self.username_input.active:
            r = self.username_input.rect
            pygame.draw.rect(game_data.ui, (120, 180, 30), pygame.rect.Rect((r.left - border, r.top - border), (r.width + border*2, r.height + border*2)))
        self.username_input.draw(game_data.ui)
        if self.password_input.active:
            r = self.password_input.rect
            pygame.draw.rect(game_data.ui, (120, 180, 30), pygame.rect.Rect((r.left - border, r.top - border), (r.width + border*2, r.height + border*2)))
        self.password_input.draw(game_data.ui)

    def validate_input(self):
        if len(self.username_input.text.text) < 5:
            self.error.text = "Username should be at least 5 characters"
            return False
        if len(self.password_input.text.text) < 5:
            self.error.text = "Password should be at least 5 characters"
            return False
        return True