import pygame
from engine.core.game_engine import GameEngine
from game.scenes.main_menu import MainMenuScene

def main():
    # create and configure the engine
    engine = GameEngine(
        width=1280,
        height=720,
        title="Tachyon",
        fps=60
    )

    # start with main menu
    engine.change_scene(MainMenuScene)

    engine.run()

if __name__ == "__main__":
    main()
