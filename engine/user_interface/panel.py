import pygame

from engine.user_interface.ui_element import UIElement


class Panel(UIElement):
    """Container for grouping UI elements."""

    def __init__(self, x: int, y: int, width: int, height: int, bg_colour: tuple = None, alpha: int = 255,
                 layer: int = 0):
        """
        Initialise a panel.
        :param x: X-axis position of the panel.
        :param y: Y-axis position of the panel.
        :param width: Width of the panel in pixels.
        :param height: Height of the panel in pixels.
        :param bg_colour: Background colour of the panel. Leave as NoneType for transparency.
        :param alpha: Alpha transparency of the panel background.
        :param layer: Z-order for rendering.
        """
        super().__init__(x, y, layer)
        self.width = width
        self.height = height
        self.bg_colour = bg_colour
        self.alpha = alpha
        self.elements: list[UIElement] = [] # List of all elements to be grouped

        if bg_colour: # Create a basic surface with the given colour
            self.surface = pygame.Surface((width, height))
            self.surface.set_alpha(alpha)
            self.surface.fill(bg_colour)
        else: # Otherwise, do not contain a surface
            self.surface = None

    def add_element(self, element: UIElement, relative_x: int = 0, relative_y: int = 0):
        """
        Add a UI element to this panel.
        :param element: The UI element to add.
        :param relative_x: X-position relative to the panel's top-left corner.
        :param relative_y: Y-position relative to the panel's top-left corner.
        """
        element.x = relative_x
        element.y = relative_y
        self.elements.append(element)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for all child elements."""
        if not self.visible:
            return False

        for element in self.elements:
            if element.handle_event(event):
                return True
        return False

    def render(self, screen: pygame.Surface) -> None:
        """Render the panel and all child elements."""
        if not self.visible:
            return None

        if self.surface:
            screen.blit(self.surface, (self.x, self.y))

        for element in self.elements:
            original_x = element.x
            original_y = element.y

            element.x = self.x + original_x
            element.y = self.y + original_y

            element.render(screen)

            element.x = original_x
            element.y = original_y