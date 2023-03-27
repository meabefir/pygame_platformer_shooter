from ImageScraper import ImageScraper
from ImageTileScraper import ImageTileScraper
import pygame

WIDTH = 1280
HEIGHT = 720

FPS = 120

WORLD_SCALE = 2
TILE_SIZE = 32 * WORLD_SCALE
IMAGE_TILE_SIZE = 32
G = 10
MAX_VERTICAL_VELOCITY = 6

screen = None
user = None
ui = pygame.Surface((WIDTH, HEIGHT))
ui.fill((255, 0, 127))
ui.set_colorkey((255, 255, 254))
render_scale = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
COLOR1 = (180, 255, 180)
COLOR2 = (110, 235, 110)

invalid_tiles = {'.': 1, '@': 1, '1': 1, '2': 1, '3': 1}
wall_tiles = {'#': 1, '<': 1, '>': 1, '%': 1}

player_scale = .24
enemy_scale = .2
gunner_scale = 2.6
images = {}

def load_data():
    global images
    images = {
        "player": {
            "gun": {
                "run": ImageScraper("assets/player/gun/run", player_scale).get(),
                "jump": ImageScraper("assets/player/gun/jump", player_scale).get(),
                "idle": ImageScraper("assets/player/gun/idle", player_scale).get(),
                "hurt": ImageScraper("assets/player/gun/hurt", player_scale).get(),
                "use": ImageScraper("assets/player/gun/shot", player_scale).get(),
            },
            "sword": {
                "run": ImageScraper("assets/player/sword/run", player_scale).get(),
                "jump": ImageScraper("assets/player/sword/jump", player_scale).get(),
                "idle": ImageScraper("assets/player/sword/idle", player_scale).get(),
                "hurt": ImageScraper("assets/player/sword/hurt", player_scale).get(),
                "use": ImageScraper("assets/player/sword/slash", player_scale).get(),
            },
            "die": ImageScraper("assets/player/die", player_scale).get(),
        },
        "enemy": {
            1: {
                "run": ImageScraper("assets/enemy1/run", enemy_scale).get(),
                "shoot": ImageScraper("assets/enemy1/shoot", enemy_scale).get(),
                "die": ImageScraper("assets/enemy1/die", enemy_scale).get(),
            },
            2: {
                "run": ImageScraper("assets/enemy2/run", enemy_scale).get(),
                "shoot": ImageScraper("assets/enemy2/shoot", enemy_scale).get(),
                "die": ImageScraper("assets/enemy2/die", enemy_scale).get(),
            },
            3: {
                "run": ImageTileScraper("assets/enemy3/run.png", scale=gunner_scale).get(),
                "shoot": ImageTileScraper("assets/enemy3/idle.png", scale=gunner_scale).get(),
                "die": ImageTileScraper("assets/enemy3/die.png", scale=gunner_scale).get(),
            },
        },
        "jungle": {
            '#': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE), ((5, 4),), WORLD_SCALE).get(),
            '<': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE), ((5, 3),), WORLD_SCALE).get(),
            '>': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE), ((5, 5),), WORLD_SCALE).get(),
            '%': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE), ((6, 4),), WORLD_SCALE).get(),
            'F': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE), ((8, 13),), WORLD_SCALE).get(),
            '$': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE),
                                  ((0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10)), WORLD_SCALE).get(),
            '/': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE),
                                  ((5, 10), (5, 11), (5, 12), (5, 13), (5, 14)), WORLD_SCALE).get(),
            'x': ImageTileScraper("assets/tiles.png", (IMAGE_TILE_SIZE, IMAGE_TILE_SIZE),
                                  ((3, 1), ), WORLD_SCALE).get(),
            'H': [pygame.transform.scale_by(pygame.image.load("assets/life.png"), .5 * WORLD_SCALE)],
            '^': [pygame.transform.scale_by(pygame.image.load("assets/ammo_box.png"), .6 * WORLD_SCALE)],
        },
    }