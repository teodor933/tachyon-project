from abc import ABC, abstractmethod
from typing import List
import pygame

class State(ABC):
    """
    Base class for all game states.
    It defines the essential methods that every state must contain.
    """
    def __init__(self, game):
        self.game = game

    def on_exit(self):
        pass

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