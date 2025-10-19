import pygame

from engine.user_interface.ui_element import UIElement


class Text(UIElement):
    """Renderable text element."""
    def __init__(self, x: int, y: int, text: str, font_size: int = 36, colour : tuple = (255, 255, 255),
                 centre_text: bool = False, layer: int = 0):
        """
        Initialise a text surface.
        :param x: X-axis position of the text.
        :param y: Y-axis position of the text.
        :param text: String content of the text element.
        :param font_size: Size of the text font.
        :param colour: Colour of the text.
        :param centre: Whether to render the text in a central position according to its coordinates.
        :param layer: Z-order for rendering.
        """
        super().__init__(x, y, layer)
        self.text = text
        self.font_size = font_size
        self.colour = colour
        self.centre_text = centre_text

        self.font = pygame.font.Font(None, font_size) # Create a font object that can be rendered
        self.font_surface = None # Variable for storing the instance's surface of the font object

        self._update_surface() # Render the text element upon initialisation

    def _update_surface(self):
        """Render the text surface."""
        self.font_surface = self.font.render(self.text, True, self.colour)

    def set_text(self, text: str):
        """Update the text content."""
        if self.text != text: # Ensure text parameter is not the same, to not waste time updating
            self.text = text # Update text content
            self._update_surface()

    def set_colour(self, colour: tuple):
        """Update the text colour."""
        if self.colour != colour: # Ensure colour parameter is not the same, to not waste time updating
            self.colour = colour # Update colour
            self._update_surface()

    def render(self, screen: pygame.Surface) -> None:
        if not self.visible or not self.font_surface:
            return None # Do not render if no surface exists or if the element is invisible

        if self.centre_text:
            rect = self.font_surface.get_rect(center=(self.x, self.y))
            screen.blit(self.font_surface, rect) # Blit/Copy the font surface onto the given screen at the centred
            # position
        else:
            screen.blit(self.font_surface, (self.x, self.y)) # Blit/Copy the font surface onto the given screen
            # at the original position

