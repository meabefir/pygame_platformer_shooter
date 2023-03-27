import pygame

import game_data
from Button import Button
from TextInput import TextInput

import database

keys_to_map = ["left", "right", "jump", "switch", "use"]
special_mappings = {
    pygame.K_SPACE: "SPACE",
}

class SettingsScreen:
    def __init__(self, back=None):
        self.back_screen = back
        self.background = pygame.Surface((game_data.WIDTH, game_data.HEIGHT))
        self.background.fill(game_data.COLOR1)

        self.title = Button(200, 100, 600, 100, game_data.COLOR2, 40, "Settings", font_color=game_data.BLACK)
        self.back_button = Button(200, 600, 120, 65, game_data.COLOR2, 32, "Back", font_color=game_data.BLACK, callback=self.back)

        self.key_binds = [Button(200, 250 + i * 65, 135, 50, game_data.COLOR2, 28, self.get_naming(k_name), font_color=game_data.BLACK) for i, k_name in enumerate(keys_to_map)]
        self.key_set = [Button(400, 250 + i * 65, 135, 50, (200, 100, 50), 28, "Bind", font_color=game_data.BLACK, callback=self.toggle_bind, params=i) for i, k_name in enumerate(keys_to_map)]

        self.binding = None

    def get_naming(self, k_name):
        return f'{k_name}: {str(chr(game_data.user[k_name]) if game_data.user[k_name] not in special_mappings else special_mappings[game_data.user[k_name]]).upper()}'

    def toggle_bind(self, idx):
        self.binding = idx

    def back(self, p=None):
        if self.back_screen is None:
            from screens.MenuScreen import MenuScreen
            self.back_screen = MenuScreen()

        game_data.screen = self.back_screen

    def select_level(self, level):
        print(level)

    def handle_event(self, event):
        self.back_button.handle_event(event)
        for kb in self.key_binds:
            kb.handle_event(event)
        for kb in self.key_set:
            kb.handle_event(event)

        if self.binding is not None:
            if event.type == pygame.KEYDOWN:
                self.update_binding(event.key)

    def update_binding(self, key):
        if key in self.get_user_keys():
            return
        game_data.user[keys_to_map[self.binding]] = key
        self.key_binds[self.binding].text = self.get_naming(keys_to_map[self.binding])
        database.udpate_binding(game_data.user["username"], keys_to_map[self.binding], key)
        self.binding = None

    def update(self, delta):
        pass

    def draw(self, screen):
        game_data.ui.blit(self.background, (0,0))

        self.title.draw(game_data.ui)

        self.back_button.draw(game_data.ui)

        for i, kb in enumerate(self.key_binds):
            if i == self.binding:
                r = kb.rect
                border = 3
                pygame.draw.rect(game_data.ui, (120, 180, 30), pygame.rect.Rect((r.left - border, r.top - border), (
                r.width + border * 2, r.height + border * 2)))
            kb.draw(game_data.ui)
        for kb in self.key_set:
            kb.draw(game_data.ui)

    def get_user_keys(self):
        u = game_data.user
        return [u[action] for action in keys_to_map]