import pygame
import random
import math
from states.base import State
from states.play import PlayState
from constants import BLACK, WHITE


class MainMenuState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.state_manager.change(PlayState(game=self.game))
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def fixed_update(self, dt_fixed: float) -> None:
        pass

    def update(self, dt) -> None:
        pass

    def render(self, screen) -> None:
        screen.fill(WHITE)
        font = pygame.font.SysFont(name="Consolas", size=48)
        text = font.render("Tachyon: Press Enter to Start", True, BLACK)
        screen.blit(text, (
            screen.get_width() // 2 - text.get_width() // 2,
            screen.get_height() // 2 - text.get_height() // 2
        ))