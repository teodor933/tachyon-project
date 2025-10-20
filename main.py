"""
Entry point for the project game.

This module initialises the game engine, registers the starting scene,
and begins the main game loop.
"""

from engine.game_engine import GameEngine
from engine.scenes.main_menu import MainMenuScene
from engine.scenes.pause_menu import PauseMenuScene
from engine.scenes.game_scene import GameScene


def main():
    """
    Initialise and run the game engine.

    Sets the initial scene to the main menu and starts the game loop.
    """
    engine = GameEngine(
        width=800,
        height=600,
        title="Tachyon",
        fps=240
    ) # Create an instance of the game engine with a configuration

    engine.scene_manager.change_scene("main_menu") # Make the initial scene the main menu scene

    engine.run() # Run the game engine loop

if __name__ == "__main__":
    # Ensures the game only runs when this file is executed directly, not when imported as a module.
    main()
