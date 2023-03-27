import pygame

import game_data
from Button import Button
from TextInput import TextInput

import database

class LeaderboardScreen:
    def __init__(self):
        self.background = pygame.Surface((game_data.WIDTH, game_data.HEIGHT))
        self.background.fill(game_data.COLOR1)

        self.page_size = 5
        self.page = 0

        self.prev_page = Button(500 + 150, 600, 75, 75, game_data.COLOR2, 32, '<', font_color=game_data.BLACK, callback=self.change_page, params=-1)
        self.next_page = Button(590 + 150, 600, 75, 75, game_data.COLOR2, 32, '>', font_color=game_data.BLACK, callback=self.change_page, params=1)

        self.title = Button(200, 100, 600, 100, game_data.COLOR2, 40, "Leaderboard", font_color=game_data.BLACK)

        self.back_button = Button(200, 600, 120, 65, game_data.COLOR2, 32, "Back", font_color=game_data.BLACK, callback=self.back)

        self.users = database.get_users()

        self.labels = [Button(410 + i * 100, 250, 80, 45, (180, 120, 50), 28, f"Lvl {i}") for i in range(6)]
        self.data = [
            [[Button(200, 300 + (i%self.page_size) * 50, 200, 45, game_data.COLOR2, 28, user[database.USER.USERNAME], font_color=game_data.BLACK)] +
             [Button(410 + ip * 100, 300 + (i%self.page_size) * 50, 80, 45, game_data.COLOR2, 28, str(points), font_color=game_data.BLACK) for ip, points in enumerate(self.get_user_points(user))]] for i, user in enumerate(self.users)
        ]
        self.data = [item for sublist in  self.data for item in sublist]

        self.max_pages = len(self.users) // self.page_size if len(self.users) % self.page_size == 0 else len(self.users) // self.page_size + 1

    def change_page(self, delta):
        if delta == -1:
            if self.page == 0:
                return
            else:
                self.page -= 1
        else:
            if self.page + 1 >= self.max_pages:
                return
            else:
                self.page += 1

    def get_user_points(self, user):
        return [user[database.USER.POINTS1+i] for i in range(6)]

    def back(self, p=None):
        from screens.MenuScreen import MenuScreen
        game_data.screen = MenuScreen()

    def select_level(self, level):
        print(level)

    def handle_event(self, event):
        self.prev_page.handle_event(event)
        self.next_page.handle_event(event)
        self.back_button.handle_event(event)

    def update(self, delta):
        pass

    def draw(self, screen):
        game_data.ui.blit(self.background, (0,0))

        self.title.draw(game_data.ui)
        self.prev_page.draw(game_data.ui)
        self.next_page.draw(game_data.ui)
        self.back_button.draw(game_data.ui)

        start_idx = self.page * self.page_size
        for row in self.data[start_idx:start_idx+self.page_size]:
            for el in row:
                el.draw(game_data.ui)
        for e in self.labels:
            e.draw(game_data.ui)