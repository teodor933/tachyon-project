import pygame
from state_manager import GameStateManager
from states import MainMenuState


class Game:
    """
    The main Game class that acts as the core engine.
    It manages the game window, clock and the state manager.
    """
    def __init__(self, screen_width: int, screen_height: int, title: str):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state_manager = GameStateManager(game=self)
        self.state_manager.change_state(MainMenuState(game=self))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000 # time taken in milliseconds converted to seconds

            events = pygame.event.get()

            self.state_manager.handle_events(events)
            self.state_manager.update(dt)
            self.state_manager.render(self.screen)

            pygame.display.flip()


