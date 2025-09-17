import pygame
from game import Game

config = {
    "screen_width": 1600,
    "screen_height": 800,
    "title": "Tachyon",
    "fps": 240
}


if __name__ == "__main__":
    pygame.init()
    game = Game(**config)
    game.run()
    pygame.quit()
