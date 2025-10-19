import pygame

from engine.user_interface.ui_element import UIElement


class Image(UIElement):
    """Renderable image element."""
    def __init__(self, x: int, y: int, image_path: str = None, surface: pygame.Surface = None,
                 centre_image: bool = False, layer: int = 0):
        """
        Initialise an image surface.
        :param x: X-axis position of the image.
        :param y: Y-axis position of the image.
        :param image_path: File path to an image file.
        :param surface: Provided surface to use instead of a file path.
        :param centre_image: Whether to render the image in a central position according to its coordinates.
        :param layer: Z-order for rendering.
        """
        super().__init__(x, y, layer)
        self.centre_image = centre_image

        if image_path: # Prioritise image files for the surface
            self.surface = pygame.image.load(image_path)
        elif surface: # If there is no image path provided, attempt at using the given surface
            self.surface = surface
        else: # No image path or provided surface
            # Create a placeholder surface
            self.surface = pygame.Surface((100, 100))
            self.surface.fill((100, 100, 100))

    def render(self, screen: pygame.Surface) -> None:
        if not self.visible: # Do not render if the element is invisible
            return None

        if self.centre_image:
            rect = self.surface.get_rect(center=(self.x, self.y))
            screen.blit(self.surface, rect) # Blit/Copy the font surface onto the given screen at the centred position
        else:
            screen.blit(self.surface, (self.x, self.y)) # Blit/Copy the font surface onto the given screen
            # at the original position