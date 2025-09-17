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

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    @abstractmethod
    def handle_events(self, events: List[pygame.event.EventType]) -> None:
        """Handle a list of pygame events."""
        raise NotImplementedError

    @abstractmethod
    def fixed_update(self, dt_fixed: float) -> None:
        """Fixed-rate update for physics and deterministic step."""
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        """Variable-rate update for non-physics logic."""
        raise NotImplementedError

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the game state onto the given screen."""
        raise NotImplementedError