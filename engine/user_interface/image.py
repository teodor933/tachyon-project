"""
Renderable image UI element with tinting, scaling, and centering support.

The Image class loads and displays images from file or surface, with options for transparency, tinting,
and smooth scaling.
"""
from typing import Optional
import pygame

from engine.user_interface.ui_element import UIElement


class Image(UIElement):
    """A renderable image UI element."""
    def __init__(self, x: int, y: int,
                 image_path: str = None,
                 surface: pygame.Surface = None,
                 centre_image: bool = False,
                 layer: int = 0,
                 element_id: Optional[str] = None,
                 alpha: int = 255):
        """
        Initialise an image element.

        Either `image_path` or `surface` must be provided.

        :param x: X-axis position of the image.
        :param y: Y-axis position of the image.
        :param image_path: File path to an image file.
        :param surface: Provided surface to use instead of a file path.
        :param centre_image: Whether to render the image in a central position according to its coordinates.
        :param layer: Z-order for rendering.
        :param element_id: Optional identifier.
        :param alpha: Opacity.
        """
        super().__init__(x, y, layer, element_id)
        self.centre_image = centre_image
        self.alpha = alpha
        self._tint_colour: Optional[tuple] = None

        # Load or create base surface
        if image_path: # Prioritise image files for the surface
            base = pygame.image.load(image_path).convert_alpha()
        elif surface: # If there is no image path provided, attempt at using the given surface
            base = surface.convert_alpha()
        else: # No image path or provided surface
            # Create a placeholder surface
            base = pygame.Surface((100, 100), pygame.SRCALPHA)
            base.fill((100, 100, 100, 255))

        self._base_surface: pygame.Surface = base
        self._render_surface: pygame.Surface = base.copy() # Ensure Pygame does not change the base in place
        self._render_surface.set_alpha(self.alpha)

    def _rebuild_render_surface(self):
        """Reapply tint and alpha to the render surface."""
        self._render_surface = self._base_surface.copy()
        if self._tint_colour is not None:
            self._render_surface.fill(self._tint_colour, special_flags=pygame.BLEND_RGBA_MULT) # Flag multiplies
            # the RGBA values of the source surface with the target surface to merge the two surfaces
        self._render_surface.set_alpha(self.alpha)

    def set_image_path(self, image_path: str) -> None:
        """Load a new image from file and update display."""
        self._base_surface = pygame.image.load(image_path).convert_alpha()
        self._rebuild_render_surface()

    def set_surface(self, surface: pygame.Surface) -> None:
        """Replace image with a new surface."""
        self._base_surface = surface.convert_alpha()
        self._rebuild_render_surface()

    def set_tint(self, colour: Optional[tuple]) -> None:
        """Apply a colour tint (multiply blend). Set None to clear."""
        self._tint_colour = colour
        self._rebuild_render_surface()

    def set_alpha(self, alpha: int) -> None:
        """Update opacity."""
        self.alpha = alpha
        self._rebuild_render_surface()

    def set_size(self, width: int, height: int) -> None:
        """Resize image with smooth scaling and preserve tint/alpha."""
        # Slower scaling but should look visually nicer
        self._render_surface = pygame.transform.smoothscale(self._base_surface, (int(width), int(height)))
        if self._tint_colour is not None:
            self._render_surface.fill(self._tint_colour, special_flags=pygame.BLEND_RGBA_MULT)
        self._render_surface.set_alpha(self.alpha)

    def get_rect(self) -> pygame.Rect:
        """Get bounding rectangle based on centering setting."""
        if self.centre_image:
            rect = self._render_surface.get_rect(center=(self.x, self.y))
        else:
            rect = self._render_surface.get_rect(topleft=(self.x, self.y))
        return rect

    def render(self, screen: pygame.Surface) -> None:
        """Draw the image if visible."""
        if not self.visible: # Do not render if the element is invisible
            return None

        if self.centre_image:
            rect = self._render_surface.get_rect(center=(self.x, self.y))
            screen.blit(self._render_surface, rect) # Blit/Copy the font surface onto the given screen at the centred position
        else:
            screen.blit(self._render_surface, (self.x, self.y)) # Blit/Copy the font surface onto the given screen
            # at the original position
