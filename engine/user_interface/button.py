from typing import Optional, Union, Callable

import pygame

from engine.user_interface.image import Image
from engine.user_interface.panel import Panel
from engine.user_interface.text import Text
from engine.user_interface.ui_element import UIElement


class Button(UIElement):
    """Interactive and renderable button element."""
    def __init__(self, x: int, y: int, width: int, height: int, on_click: Callable, text: str = "", font_size: int = 36,
                 text_colour: tuple = (255, 255, 255), normal_colour: tuple = (100, 100, 100),
                 hover_colour: tuple = (150, 150, 150), pressed_colour: tuple = (80, 80, 80), centre_text: bool = False,
                 centre_surface: bool = False, layer: int = 0):
        """
        Initialise a button surface containing a text surface, with on click event handling.
        :param x: X-axis position of the button.
        :param y: Y-axis position of the button.
        :param width: Width of the button surface in pixels.
        :param height: Height of the button surface in pixels.
        :param on_click: Callable function for when interacting with the button element.
        :param text: The displayed string on the button surface.
        :param font_size: Size of the text font.
        :param text_colour: Colour of the text.
        :param normal_colour: Background colour when not interacting.
        :param hover_colour: Background colour when hovering.
        :param pressed_colour: Background colour when pressed.
        :param centre_text: Whether to centre the text in the button.
        :param centre_surface: Whether to centre the surface relating to the button's position.
        :param layer: Z-order for rendering.
        """
        super().__init__(x, y, layer)
        self.width = width
        self.height = height
        self.centre_surface = centre_surface
        self.on_click = on_click # Store function to run when clicking the button

        self.normal_colour = normal_colour  # Colour for the button surface with no events
        self.hover_colour = hover_colour  # Colour for the button surface when mouse is hovering
        self.pressed_colour = pressed_colour  # Colour for the button surface when button is pressed
        self.current_colour = normal_colour  # Set default colour of the surface to the normal colour

        self.is_hovered = False
        self.is_pressed = False

        if self.centre_surface: # Calculate the actual top-left position for the panel to pass
            panel_x = x - width // 2
            panel_y = y - width // 2
        else:
            panel_x = x
            panel_y = y

        self.panel = Panel(
            x=panel_x,
            y=panel_y,
            width=width,
            height=height,
            bg_colour=normal_colour,
            layer=layer
        )

        if centre_text: # Calculate relative position of the text to the surface
            text_x = width // 2
            text_y = height // 2
        else: # Small number padding so the text is not on the edge of the surface
            text_x = 10
            text_y = 10

        self.text_element = Text(x=0, # Will be set by add_element now
                                 y=0,
                                 text=text,
                                 font_size=font_size,
                                 colour=text_colour,
                                 centre_text=centre_text,
                                 layer=0 # Ensure text is rendered above the button element
                                 )

        self.panel.add_element(self.text_element, text_x, text_y) # Add text to the panel with relative coordinates

        self._update_surface()

        print(f"Button center coords: ({x}, {y})")
        print(f"Panel position: ({panel_x}, {panel_y})")
        print(f"Button rect: {self._get_button_rect()}")

    def _update_surface(self    ):
        """Update the button surface based on the current state."""
        if self.is_pressed:
            self.current_colour = self.pressed_colour
        elif self.is_hovered:
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.normal_colour

        self.panel.bg_colour = self.current_colour # Change stored colour value
        self.panel.surface.fill(self.current_colour) # Fill the surface with a colour

        # Add a border to the button
        pygame.draw.rect(self.panel.surface, (0, 0, 0), (0, 0, self.width, self.height), 2)

    def _get_button_rect(self):
        """Get the actual button rectangle in screen coordinates."""
        return pygame.Rect(self.panel.x, self.panel.y, self.width, self.height)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for the button."""
        button_rect = self._get_button_rect()

        if event.type == pygame.MOUSEMOTION: # General mouse movement
            mouse_x, mouse_y = event.pos # Gather its current coordinates
            was_hovered = self.is_hovered # Store current state as previous to update
            self.is_hovered = button_rect.collidepoint(mouse_x, mouse_y) # Update current state if the mouse is inside
            # the button's region

            if was_hovered != self.is_hovered: # Only update the surface if the surface state is changing
                self._update_surface()
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN: # Check if we pressed a mouse button
            if event.button == 1: # Left click input
                mouse_x, mouse_y = event.pos
                if button_rect.collidepoint(mouse_x, mouse_y): # Check if inside the button's region
                    self.is_pressed = True
                    self._update_surface()
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:  # Left click release
                self.is_pressed = False # As long as the mouse is held down, the button will appear as if its
                # being pressed
                self._update_surface()

                # Check if mouse is still over button to finish the click, if we move outside the button's region,
                # act as if the user did not mean to interact with the button
                mouse_x, mouse_y = event.pos
                if button_rect.collidepoint(mouse_x, mouse_y): # Check if inside button region
                    if self.on_click: # If a click function exists, call it
                        self.on_click()
                    return True

        return False # Did not consume event

    def render(self, screen: pygame.Surface) -> None:
        """Render the button to the screen."""
        if not self.visible: # Do not render if the element is invisible
            return None

        self.panel.render(screen)

    def set_text(self, text: str):
        """Update the button text content."""
        self.text_element.set_text(text)

    def set_on_click_func(self, on_click: Callable):
        """Update the button callback function."""
        self.on_click = on_click





