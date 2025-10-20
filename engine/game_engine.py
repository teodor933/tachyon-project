"""
Core game engine responsible for the main loop and window management.

Initialises Pygame, manages the display, and coordinates scene updates.
"""
import pygame # Import the Pygame library

from engine.scene_manager import SceneManager


class GameEngine:
    """Main game engine class."""
    def __init__(self, width: int = 800, height: int = 600, title: str = "Tachyon Engine", fps: int = 60):
        """
        Initialise the game engine and Pygame subsystems.
        :param width: The width of the game window in pixels.
        :param height: The height of the game window in pixels.
        :param title: The title displayed on the game window.
        :param fps: The target frames per second for the main loop.
        """
        pygame.init() # Initialise all imported Pygame modules

        self.screen = pygame.display.set_mode((width, height)) # Create the main display surface with given resolution
        pygame.display.set_caption(title) # Set the title of the window

        self._clock = pygame.time.Clock() # Create a Clock object to manage the frame rate
        self._running = True # Control variable for the main game loop
        self._fps = fps # Control variable for the frame rate limit

        self.scene_manager = SceneManager(self) # Create an instance of a scene manager

    def run(self):
        """
        Start the main game loop.

        Handles events, updates, and rendering until the window is closed.
        """
        while self._running:
            dt = self._clock.tick(self._fps) / 1000.0 # Pause briefly to cap the frame rate at 60 FPS and converts
            # delta time to seconds

            events = pygame.event.get()

            for event in events:  # Loop through a list of all pending events
                if event.type == pygame.QUIT:  # Check if the user closed the window
                    self._running = False  # End the main loop

            self.scene_manager.handle_events(events) # Call the handle events method of the current scene
            self.scene_manager.update(dt) # Call the update method of the current scene
            self.scene_manager.render() # Call render method of the current scene

            pygame.display.flip()  # Update the entire screen with everything drawn this frame

        pygame.quit() # Clean up Pygame resources

    def set_is_running(self, is_running: bool):
        """
        Set to true for the game to stop.
        """
        self._running = is_running
