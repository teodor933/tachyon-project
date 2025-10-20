"""
Base class for all user interface elements.

Provides common properties like position, visibility, layering, and hitbox management.
All UI elements must inherit from this class.
"""
from abc import ABC, abstractmethod
from typing import Optional, Union

import pygame


class UIElement(ABC):
    """Base class for all UI elements."""
    def __init__(self, x: int, y: int,
                 layer: int = 0,
                 element_id: Optional[str] = None):
        """
        Initialise a UI element.
        :param x: X-axis position of the element.
        :param y: Y-axis position of the element.
        :param layer: Z-order for rendering.
        :param element_id: Unique identifier for sorting and lookups.
        """
        self.x = x # X coordinate position
        self.y = y # Y coordinate position
        self.layer = layer # Z coordinate position
        self.visible = True # Whether this element should be rendered or not
        self.enabled = True  # Whether this element can interact/handle events
        self.id = element_id  # Optional identifier for lookup
        self._hitbox_rect_override: Optional[pygame.Rect] = None # Optional overrider to define a hitbox
        # separate to the visuals

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """
        Draw the element on the screen.
        :param screen: Target surface to render onto.
        """
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Process a Pygame event.

        Override to add interactivity.
        :param event: The event to handle.
        :return: True if the event was consumed.
        """
        return False

    def update(self, dt: float) -> None:
        """
        Update element state.

        Override for dynamic behaviour.
        :param dt: Delta time in seconds.
        """
        return None

    def get_rect(self) -> pygame.Rect:
        """
        Get the visual bounding rectangle.
        Subclasses should override to return accurate bounds.
        :return: Bounding rectangle in screen coordinates.
        """
        return pygame.Rect(self.x, self.y, 0, 0)

    def get_hitbox_rect(self) -> pygame.Rect:
        """
        Get the interactive hitbox rectangle.

        Defaults to visual rect unless overridden.
        :return: Interactive area.
        """
        return self._hitbox_rect_override or self.get_rect()

    def set_hitbox_rect(self, rect: Union[pygame.Rect, tuple[int, int, int, int], None]) -> None:
        """
        Set or clear a custom hitbox.
        :param rect: New hitbox as Rect, tuple, or None to clear.
        """
        if rect is None: # Left argument empty
            self._hitbox_rect_override = None # Clear the hitbox override
        else:
            self._hitbox_rect_override = pygame.Rect(rect) # Replace the hitbox override

    def set_position(self, x: int, y: int) -> None:
        """Set the element's position."""
        self.x = x
        self.y = y

    def get_position(self) -> tuple[int, int]:
        """Get the element's position."""
        return self.x, self.y

    def set_visible(self, visible: bool) -> None:
        """Set visibility."""
        self.visible = bool(visible)

    def is_visible(self) -> bool:
        """Check if visible."""
        return self.visible

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable interaction."""
        self.enabled = bool(enabled)

    def is_enabled(self) -> bool:
        """Check if enabled."""
        return self.enabled

    def set_layer(self, layer: int) -> None:
        """Set rendering layer."""
        self.layer = int(layer)

    def get_layer(self) -> int:
        """Get rendering layer."""
        return self.layer
