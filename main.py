import pygame

import game_data
from game_data import *

from PhysicsManager import PhysicsManager
from screens.MenuScreen import MenuScreen
from screens.LevelScreen import LevelScreen
from screens.LoginScreen import LoginScreen

from AnimatedSprite import AnimatedSprite
from ImageScraper import ImageScraper
from ImageTileScraper import ImageTileScraper
from Level import Level

import sound
import database

# Initialize Pygame
pygame.init()

# Set the screen size
display = pygame.display.set_mode((WIDTH, HEIGHT))
game_data.load_data()
pygame.display.set_caption('Save The Jungle')

current_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

sound.init_sound()
PhysicsManager.init()

# game_data.screen = LevelScreen(Level())
game_data.screen = LoginScreen()


test = None
# test = AnimatedSprite(ImageScraper("assets/player/gun/run", .2).get(), .6, True)
# test = AnimatedSprite(ImageTileScraper("assets/tiles.png", (32, 32), ((0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10)), 1).get(), .6, True)
# test = Level()

# render_surface = pygame.Surface((WIDTH / render_scale, HEIGHT / render_scale))
render_surface = pygame.Surface((WIDTH, HEIGHT))

# Run the game loop
running = True
while running:
    new_time = pygame.time.get_ticks()
    # delta_time = (new_time - current_time) / 1000
    delta_time = 1 / FPS
    current_time = new_time

    for event in pygame.event.get():
        if game_data.screen is not None:
            game_data.screen.handle_event(event)
        if test is not None:
            test.handle_event(event)

        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     print(event.key)

    render_surface.fill((0, 0, 0))
    game_data.ui.fill(game_data.ui.get_colorkey())
    if game_data.screen is not None:
        game_data.screen.update(delta_time)
        game_data.screen.draw(render_surface)

    if test is not None:
        test.update(delta_time)
        test.draw(render_surface)

    scaled_render_surface = pygame.transform.scale_by(render_surface, render_scale)
    # display.blit(scaled_render_surface, (0, 0), game_data.main_camera)
    display.blit(scaled_render_surface, (0, 0))
    display.blit(game_data.ui, (0, 0))

    # Update the screen
    # pygame.display.update()
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
database.close()