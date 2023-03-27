import pygame

sounds = {}

def init_sound():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(100)

    # menu = pygame.mixer.Sound("assets/music/menu.wav")
    sounds["menu"] = pygame.mixer.Sound("assets/music/menu.ogg")
    sounds["menu"].set_volume(.5)

    sounds["jungle"] = pygame.mixer.Sound("assets/music/jungle.ogg")
    sounds["jungle"].set_volume(.5)

    sounds["player_shoot"] = pygame.mixer.Sound("assets/music/gun.ogg")
    sounds["player_shoot"].set_volume(.5)

    sounds["9mm"] = pygame.mixer.Sound("assets/music/9mm.ogg")
    sounds["9mm"].set_volume(.5)

    sounds["fireball"] = pygame.mixer.Sound("assets/music/fireball.ogg")
    sounds["fireball"].set_volume(.5)

    sounds["slash"] = pygame.mixer.Sound("assets/music/slash.ogg")
    sounds["slash"].set_volume(.5)

    sounds["squish"] = pygame.mixer.Sound("assets/music/squish.ogg")
    sounds["squish"].set_volume(.5)


def play(name, overlap=False):
    sound = sounds[name]

    if not overlap:
        for id in range(pygame.mixer.get_num_channels()):
            vc = pygame.mixer.Channel(id)

            if sound == vc.get_sound():
                return

    pygame.mixer.Sound.play(sound)

def stop(name):
    pygame.mixer.Sound.stop(sounds[name])
