from abc import ABC, abstractmethod

import pygame


class UIElement(ABC):
    """Base class for all UI elements."""
    def __init__(self, x: int, y: int, layer: int = 0):
        self.x = x # X coordinate position
        self.y = y # Y coordinate position
        self.layer = layer # Z coordinate position
        self.visible = True # Whether this element should be rendered or not

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the UI element."""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle an event. Return True if the event was fully handled."""
        return False
