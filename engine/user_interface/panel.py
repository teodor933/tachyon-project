"""
Container UI element for grouping and rendering child elements.

Panels provide a background surface with optional borders and manage relative positioning of child UI elements.
"""
from typing import Optional
import pygame

from engine.user_interface.ui_element import UIElement


class Panel(UIElement):
    """A container for grouping and rendering multiple UI elements."""

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 bg_colour: tuple = None,
                 alpha: int = 255,
                 layer: int = 0,
                 border_colour: tuple = None,
                 border_width: int = 0,
                 border_radius: int = 0
                 ):
        """
        Initialise a panel.

        :param x: X-axis position of the panel.
        :param y: Y-axis position of the panel.
        :param width: Width of the panel in pixels.
        :param height: Height of the panel in pixels.
        :param bg_colour: Background colour of the panel. Leave as None for transparent.
        :param alpha: Alpha transparency of the panel background.
        :param layer: Z-order for rendering.
        :param border_colour: Optional border colour.
        :param border_width: Optional border width in pixels.
        :param border_radius: Optional border radius.
        """
        super().__init__(x, y, layer)
        self.width = width
        self.height = height
        self.bg_colour = bg_colour
        self.alpha = alpha
        self.border_colour = border_colour
        self.border_width = border_width
        self.border_radius = border_radius
        self.elements: list[UIElement] = [] # List of all elements to be grouped

        # Create transparent surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA) # SRCALPHA supports per-pixel
        # alpha transparency
        self.surface.set_alpha(alpha)
        self._rebuild_background()

    def _rebuild_background(self):
        """Redraw the panel background and border."""
        self.surface.fill((0, 0, 0, 0)) # Clear with full transparency
        if self.bg_colour:
            pygame.draw.rect(
                self.surface,
                self.bg_colour,
                (0, 0, self.width, self.height),
                border_radius=self.border_radius
            )
        if self.border_colour and self.border_width > 0:
            pygame.draw.rect(
                self.surface,
                self.border_colour,
                (0, 0, self.width, self.height),
                width=self.border_width,
                border_radius=self.border_radius
            )

    def set_size(self, width: int, height: int):
        """Resize the panel surface and rebuild its surface."""
        width = int(width)
        height = int(height)
        if width == self.width and height == self.height:
            return None # No need to update the size
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)
        self._rebuild_background()

    def get_size(self) -> tuple[int, int]:
        """Get current panel dimensions."""
        return self.width, self.height

    def set_bg_colour(self, colour: Optional[tuple]) -> None:
        """Update background colour and redraw."""
        self.bg_colour = colour
        self._rebuild_background()

    def get_bg_colour(self) -> Optional[tuple]:
        """Get current background colour."""
        return self.bg_colour

    def set_alpha(self, alpha: int) -> None:
        """Update opacity."""
        self.alpha = alpha
        self.surface.set_alpha(alpha)

    def add_element(self, element: UIElement, relative_x: int = 0, relative_y: int = 0):
        """
        Add a child UI element with relative positioning.

        :param element: Child element to add.
        :param relative_x: X-position relative to the panel's top-left corner.
        :param relative_y: Y-position relative to the panel's top-left corner.
        """
        element.x = relative_x
        element.y = relative_y
        self.elements.append(element)
        return element

    def clear_elements(self) -> None:
        """Remove all child elements."""
        self.elements.clear()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for all child elements."""
        if not self.visible or not self.enabled:
            return False

        # Run the event handling for each child element
        for element in sorted(self.elements, key=lambda elem: elem.layer, reverse=True):
            if element.handle_event(event):
                return True
        return False

    def render(self, screen: pygame.Surface) -> None:
        """Render panel background and all child elements."""
        if not self.visible:
            return None

        # Draw a panel background
        screen.blit(self.surface, (self.x, self.y))

        # Render children with absolute positioning
        for element in self.elements:
            original_x = element.x # Store current relative coordinates
            original_y = element.y

            element.x = self.x + original_x # Convert relative coordinates to absolute
            element.y = self.y + original_y

            element.render(screen) # Pass absolute screen coordinates to render on the screen

            element.x = original_x # Convert absolute coordinates to relative to keep track of the relative position
            element.y = original_y

    def get_rect(self) -> pygame.Rect:
        """Get bounding rectangle of the panel."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
