"""
Renderable text UI element with support for wrapping, alignment, and styling.

The Text class handles dynamic rendering of strings with customisable fonts, colours, alignment,
and optional word wrapping within a maximum width.
"""

from typing import Optional
import pygame

from engine.user_interface.ui_element import UIElement


class Text(UIElement):
    """Renderable text element."""
    def __init__(self, x: int, y: int,
                 text: str,
                 font_size: int = 36,
                 colour: tuple = (255, 255, 255),
                 centre_text: bool = False,
                 layer: int = 0,
                 font_path: Optional[str] = None,
                 max_width: Optional[int] = None,
                 align: Optional[str] = None,
                 element_id: Optional[str] = None,
                 alpha: int = 255):
        """
        Initialise a text UI element.

        :param x: X-axis position of the text.
        :param y: Y-axis position of the text.
        :param text: String content of the text element.
        :param font_size: Size of the text font.
        :param colour: Colour of the text.
        :param centre: Whether to render the text in a central position according to its coordinates.
        :param layer: Z-order for rendering.
        :param font_path: Optional path to a font file.
        :param max_width: Optional max width for wrapping around.
        :param align: Optional text alignment: "left", "centre", "right". If None, uses centre_text.
        :param element_id: Optional identifier.
        :param alpha: Opacity.
        """
        super().__init__(x, y, layer, element_id)
        self.text = text
        self.font_size = font_size
        self.colour = colour
        self.centre_text = centre_text
        self.max_width = max_width
        self.align = align
        self.alpha = alpha
        self.font_path = font_path

        # Create a font object that can be rendered
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
        self.font_surface: Optional[pygame.Surface] = None # Variable for storing the instance's surface of the font object

        self._update_surface() # Render the text element upon initialisation

    def _wrap_text(self, text: str, max_width: int) -> list[pygame.Surface]:
        """
        Split text into lines that fit within a given width.
        :param text: Input string to wrap.
        :param max_width: Maximum allowed line width in pixels.
        :return: List of rendered line surfaces.
        """
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            width, _ = self.font.size(test) # Returns the width and height of the font in pixels
            if width <= max_width or not current:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)

        # Render each line and apply alpha
        rendered = [self.font.render(line, True, self.colour) for line in lines]
        for surface in rendered:
            surface.set_alpha(self.alpha)
        return rendered

    def _update_surface(self):
        """Re-render the text surface based on current properties."""
        if self.max_width:
            lines = self._wrap_text(self.text, self.max_width)
            if not lines:
                self.font_surface = None
                return None

            width = max(surface.get_width() for surface in lines)
            height = sum(surface.get_height() for surface in lines)
            surf = pygame.Surface((width, height), pygame.SRCALPHA)

            y = 0
            for surface in lines:
                surf.blit(surface, (0, y))
                y += surface.get_height()
            surf.set_alpha(self.alpha)
            self.font_surface = surf
        else:
            surf = self.font.render(self.text, True, self.colour)
            surf.set_alpha(self.alpha)
            self.font_surface = surf

    def set_text(self, text: str):
        """Update the displayed text and re-render if changed."""
        if self.text != text: # Ensure text parameter is not the same, to not waste time updating
            self.text = text # Update text content
            self._update_surface()

    def set_colour(self, colour: tuple):
        """Update text colour and re-render if changed."""
        if self.colour != colour: # Ensure colour parameter is not the same, to not waste time updating
            self.colour = colour # Update colour
            self._update_surface()

    def set_font_size(self, size: int):
        """Change font size and re-render."""
        self.font_size = int(size)
        self.font = pygame.font.Font(self.font_path if self.font_path else None, self.font_size)
        self._update_surface()

    def set_font(self, font_path: Optional[str]):
        """Switch to a new font file and re-render."""
        self.font = pygame.font.Font(font_path, self.font_size)
        self.font_path = font_path
        self._update_surface()

    def set_max_width(self, max_width: Optional[int]):
        """Enable or disable word wrapping."""
        self.max_width = max_width
        self._update_surface()

    def set_alignment(self, align: Optional[str] = None, centre_flag: Optional[bool] = None):
        """Update text alignment settings."""
        if align is not None:
            self.align = align
        if centre_flag is not None:
            self.centre_text = bool(centre_flag)

    def set_alpha(self, alpha: int):
        """Set opacity and re-render."""
        self.alpha = alpha
        self._update_surface()

    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the rendered text.

        Uses alignment settings to determine anchor point.
        :return: Bounding rectangle in screen coordinates.
        """
        if not self.font_surface:
            return pygame.Rect(self.x, self.y, 0, 0)
        if (self.align == "centre") or (self.align is None and self.centre_text):
            rect = self.font_surface.get_rect(center=(self.x, self.y))
        elif self.align == "right":
            rect = self.font_surface.get_rect(midright=(self.x, self.y))
        elif self.align == "left":
            rect = self.font_surface.get_rect(midleft=(self.x, self.y))
        else:
            rect = self.font_surface.get_rect(topleft=(self.x, self.y))
        return rect

    def render(self, screen: pygame.Surface) -> None:
        """Draw the text onto the screen if visible."""
        if not self.visible or not self.font_surface:
            return None # Do not render if no surface exists or if the element is invisible

        rect = self.get_rect()
        screen.blit(self.font_surface, rect) # Blit/Copy the font surface onto the given screen
        # at the given position
