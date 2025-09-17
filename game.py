import pygame

from constants import MAX_FPS, PHYSICS_HZ
from core.state_manager import GameStateManager
from states.main_menu import MainMenuState


class Game:
    """
    The main Game class that acts as the core engine.
    It manages the game window, clock and the state manager.
    """
    def __init__(self, **kwargs):
        width = kwargs.get("screen_width", 1920)
        height = kwargs.get("screen_height", 1080)
        title = kwargs.get("title", "Tachyon")
        self.fps = kwargs.get("fps", MAX_FPS)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state_manager = GameStateManager(game=self)
        self.state_manager.change(MainMenuState(game=self))

        self._dt_fixed = 1.0 / float(PHYSICS_HZ)
        self._accumulator = 0.0

    def run(self):
        while self.running:
            dt_raw = self.clock.tick(self.fps) / 1000.0
            dt_raw = min(dt_raw, 0.25)

            #dt = self.clock.tick(60) / 1000 # time taken in milliseconds converted to seconds

            events = pygame.event.get()
            self.state_manager.handle_events(events)

            self._accumulator += dt_raw
            while self._accumulator >= self._dt_fixed:
                self.state_manager.fixed_update(self._dt_fixed)
                self._accumulator -= self._dt_fixed

            self.state_manager.update(dt_raw)
            self.state_manager.render(self.screen)

            pygame.display.flip()


