import pygame
from core.state_manager import GameStateManager
from states.main_menu import MainMenuState


class Game:
    """
    The main Game class that acts as the core engine.
    It manages the game window, clock and the state manager.
    """
    def __init__(self, **kwargs):
        self.screen = pygame.display.set_mode((kwargs.get("screen_width", 1920), kwargs.get("screen_height", 1920)))
        pygame.display.set_caption(kwargs.get("title", "Tachyon"))
        self.fps = kwargs.get("fps", 60)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state_manager = GameStateManager(game=self)
        self.state_manager.change(MainMenuState(game=self))

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000 # time taken in milliseconds converted to seconds

            events = pygame.event.get()

            self.state_manager.handle_events(events)
            self.state_manager.update(dt)
            self.state_manager.render(self.screen)

            pygame.display.flip()


