import pygame
from states.base import State
from constants import GREEN

class PlayState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(GREEN)