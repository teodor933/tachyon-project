import pygame
from game import Game

pygame.quit()

if __name__ == "__main__":
    pygame.init()
    game = Game(screen_width=1920, screen_height=1080, title="Tachyon")
    game.run()
    pygame.quit()
