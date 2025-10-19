from engine.game_engine import GameEngine # Import the GameEngine class from the defined file
from engine.scenes.main_menu import MainMenuScene


def main():
    engine = GameEngine(
        width=1920,
        height=1080,
        title="Tachyon",
        fps=60
    ) # Create an instance of the game engine with a configuration

    engine.scene_manager.change_scene("main_menu") # Make the initial scene the main menu scene

    engine.run() # Run the game engine loop

if __name__ == "__main__": # Define entry point to avoid code running on imports
    main()

