import pygame
from states.base import State
from constants import GREEN

class PlayState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def fixed_update(self, dt_fixed: float) -> None:
        pass

    def update(self, dt) -> None:
        pass

    def render(self, screen) -> None:
        screen.fill(GREEN)