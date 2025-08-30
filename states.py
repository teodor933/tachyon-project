from abc import abstractmethod, ABC
from typing import List
import pygame
from constants import GREEN, WHITE, BLACK

class State(ABC):
    """
    Base class for all game states.
    It defines the essential methods that every state must contain.
    """
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self, events: List[pygame.event.EventType]) -> None:
        """Handle a list of pygame events."""
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the game state. dt is delta time in seconds."""
        raise NotImplementedError

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the game state onto the given screen."""
        raise NotImplementedError


class MainMenuState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.state_manager.change_state(PlayState(game=self.game))

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(WHITE)
        font = pygame.font.SysFont(name="Arial", size=48)
        text = font.render("Press Enter to Start", True, BLACK)
        screen.blit(text, (800, 500))

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