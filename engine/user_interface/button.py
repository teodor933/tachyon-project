"""
Interactive button UI element with visual states, optional image support, and hover expansion.

The Button class combines a background (colour or image), optional border, and centered or padded text.
It supports three interaction states: normal, hover, and pressed.
"""
from typing import Optional, Callable

import pygame

from engine.user_interface.animator import Tween
from engine.user_interface.image import Image
from engine.user_interface.panel import Panel
from engine.user_interface.text import Text
from engine.user_interface.ui_element import UIElement


class Button(UIElement):
    """An interactive and animated button UI element."""
    def __init__(self, x: int, y: int,
                 width: int,
                 height: int,
                 on_click: Optional[Callable] = None,
                 text: str = "",
                 font_size: int = 36,
                 text_colour: tuple = (255, 255, 255),
                 normal_colour: tuple = (100, 100, 100),
                 hover_colour: tuple = (150, 150, 150),
                 pressed_colour: tuple = (80, 80, 80),
                 centre_text: bool = False,
                 centre_surface: bool = False,
                 layer: int = 0,
                 normal_image_path: Optional[str] = None,
                 hover_image_path: Optional[str] = None,
                 pressed_image_path: Optional[str] = None,
                 border_colour: Optional[tuple] = (0, 0, 0),
                 border_width: int = 2,
                 border_radius: int = 0,
                 hover_tint: Optional[tuple] = None,
                 padding: int = 10,
                 expand_on_hover: bool = False,
                 expanded_width: Optional[int] = None,
                 expansion_duration: float = 0.2,
                 expansion_ease: str = "ease_out",
                 element_id: Optional[str] = None,
                 ):
        """
        Initialise a fully interactive button.

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
        :param normal_image_path: Optional PNG path for normal state background.
        :param hover_image_path: Optional PNG path for hover state background.
        :param pressed_image_path: Optional PNG path for pressed state background.
        :param border_colour: Optional border colour.
        :param border_width: Optional border width.
        :param border_radius: Optional border radius for rounded corners.
        :param hover_tint: Optional RGB tint applied when hovered.
        :param padding: Left/top padding for text when not centered.
        :param expand_on_hover: If True, the visual expands horizontally on hover.
        :param expanded_width: The target width when expanded. Defaults to width if not provided.
        :param expansion_duration: Seconds for expand/retract animation.
        :param expansion_ease: Easing name for expansion tween.
        :param element_id: Optional identifier.
        """
        super().__init__(x, y, layer, element_id)
        self.base_width = int(width)
        self.height = int(height)
        self.centre_surface = centre_surface
        self.on_click = on_click # Store function to run when clicking the button

        self.normal_colour = normal_colour  # Colour for the button surface with no events
        self.hover_colour = hover_colour  # Colour for the button surface when mouse is hovering
        self.pressed_colour = pressed_colour  # Colour for the button surface when button is pressed
        self.current_colour = normal_colour  # Set default colour of the surface to the normal colour

        self.normal_image = pygame.image.load(normal_image_path).convert_alpha() if normal_image_path else None
        self.hover_image = pygame.image.load(hover_image_path).convert_alpha() if hover_image_path else None
        self.pressed_image = pygame.image.load(pressed_image_path).convert_alpha() if pressed_image_path else None

        self.border_colour = border_colour
        self.border_width = border_width
        self.border_radius = border_radius
        self.hover_tint = hover_tint
        self.padding = int(padding)

        self.is_hovered = False
        self.is_pressed = False
        self._disabled = False

        self.expand_on_hover = expand_on_hover
        self.expanded_width = int(expanded_width) if expanded_width else self.base_width
        self._current_width = float(self.base_width)
        self._expand_tween = Tween(0.0)  # 0.0 = collapsed, 1.0 = expanded
        self._expansion_duration = float(expansion_duration)
        self._expansion_ease = expansion_ease

        if self.centre_surface: # Calculate the actual top-left position for the panel to pass
            panel_x = x - self.base_width // 2
            panel_y = y - self.height // 2
        else:
            panel_x = x
            panel_y = y

        self.panel = Panel(
            x=panel_x,
            y=panel_y,
            width=self.base_width,
            height=self.height,
            bg_colour=self.normal_colour if self.normal_image is None else None,
            layer=layer,
            border_colour=self.border_colour,
            border_width=self.border_width,
            border_radius=self.border_radius
        )

        # Create and add text
        self.text_element = Text(
            x=0, # Will be set by add_element now
            y=0,
            text=text,
            font_size=font_size,
            colour=text_colour,
            centre_text=centre_text,
            layer=layer + 1 # Ensure text is rendered above the button element
        )

        # Add text to the panel with initial relative coordinates. It will be re-laid-out during render
        self.panel.add_element(self.text_element,
                               # Calculate relative position of the text to the surface
                               self.base_width // 2 if centre_text else self.padding,
                               self.height // 2 if centre_text else self.padding)

        # Fixed hitbox defines interaction regardless of visual expansion
        # Always equal to the base size at panel's position
        self.set_hitbox_rect(pygame.Rect(self.panel.x, self.panel.y, self.base_width, self.height))

        self._redraw_background()

    def set_text(self, text: str):
        """Update the button's label."""
        self.text_element.set_text(text)

    def set_text_colour(self, colour: tuple):
        """Update the label colour."""
        self.text_element.set_colour(colour)

    def set_on_click_func(self, on_click: Optional[Callable]):
        """Assign a new click handler."""
        self.on_click = on_click

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable interaction."""
        super().set_enabled(enabled)
        self._disabled = not enabled

    def set_colours(self, normal: Optional[tuple] = None,
                    hover: Optional[tuple] = None,
                    pressed: Optional[tuple] = None):
        """Update state colours and redraw."""
        if normal is not None:
            self.normal_colour = normal
        if hover is not None:
            self.hover_colour = hover
        if pressed is not None:
            self.pressed_colour = pressed
        self._redraw_background()

    def set_images(self, normal: Optional[pygame.Surface] = None,
                   hover: Optional[pygame.Surface] = None,
                   pressed: Optional[pygame.Surface] = None):
        """Replace state images and redraw."""
        self.normal_image = normal
        self.hover_image = hover
        self.pressed_image = pressed
        self._redraw_background()

    def set_expand_behaviour(self, enabled: bool, expanded_width: Optional[int] = None,
                            duration: Optional[float] = None, ease: Optional[str] = None):
        """Configure hover expansion animation."""
        self.expand_on_hover = bool(enabled)
        if expanded_width is not None:
            self.expanded_width = int(expanded_width)
        if duration is not None:
            self._expansion_duration = float(duration)
        if ease is not None:
            self._expansion_ease = ease

    def _state_image(self) -> Optional[pygame.Surface]:
        """Get the appropriate background image for the current state."""
        if self.is_pressed and self.pressed_image is not None:
            return self.pressed_image
        if self.is_hovered and self.hover_image is not None:
            return self.hover_image
        return self.normal_image

    def _state_colour(self) -> tuple:
        """Get the appropriate background colour for the current state."""
        if self.is_pressed:
            return self.pressed_colour
        if self.is_hovered:
            return self.hover_colour
        return self.normal_colour

    def _redraw_background(self):
        """Redraw the button panel based on current state and size."""
        self.panel.set_size(int(self._current_width), self.height) # Set panel size to current width

        image = self._state_image() # Base fill
        if image is not None:
            scaled_image = pygame.transform.smoothscale(image, (int(self._current_width), self.height))
            self.panel.surface.blit(scaled_image, (0, 0))
        else:
            self.panel.set_bg_colour(self._state_colour())

        if self.is_hovered and self.hover_tint is not None: # Optional hover tint on top
            tint_surface = pygame.Surface((int(self._current_width), self.height), pygame.SRCALPHA)
            r, g, b = self.hover_tint
            tint_surface.fill((r, g, b, 60))
            self.panel.surface.blit(tint_surface, (0, 0))

    def _layout_text(self):
        """Reposition text based on current visual width and alignment."""
        width = int(self._current_width)

        if self.text_element.centre_text: # Vertical placement
            text_y = self.height // 2
        else:
            text_y = self.padding

        if self.text_element.centre_text: # Horizontal placement
            # Centre horizontally within the visual width
            # When centre_text=True, Text uses centre alignment, so set its (x, y) as the centre
            self.text_element.x = width // 2
            self.text_element.y = text_y
        else:
            # Left padding
            self.text_element.x = self.padding
            self.text_element.y = text_y

    def _button_hitbox_rect(self) -> pygame.Rect:
        """Return the fixed interaction area (base size)."""
        return pygame.Rect(self.panel.x, self.panel.y, self.base_width, self.height)

    def _visual_rect(self) -> pygame.Rect:
        """Return the current visual bounds (can be expanded)."""
        return pygame.Rect(self.panel.x, self.panel.y, int(self._current_width), self.height)

    def get_rect(self) -> pygame.Rect:
        """Get visual rectangle."""
        return self._visual_rect()

    def get_hitbox_rect(self) -> pygame.Rect:
        """Get interaction rectangle (fixed)."""
        # Always use a static base hitbox so interactions are consistent
        return self._button_hitbox_rect()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process mouse events for hover and click detection."""
        if not self.visible or not self.enabled:
            return False

        button_hitbox = self._button_hitbox_rect()

        if event.type == pygame.MOUSEMOTION: # General mouse movement
            mouse_x, mouse_y = event.pos # Gather its current coordinates
            prev_hover = self.is_hovered # Store current state as previous to update
            self.is_hovered = button_hitbox.collidepoint(mouse_x, mouse_y) # Update current state if the mouse is inside
            # the button's region

            if prev_hover != self.is_hovered: # Only update the surface if the surface state is changing
                # Kick off expansion tween if needed
                if self.expand_on_hover:
                    target = 1.0 if self.is_hovered else 0.0
                    self._expand_tween.to(target, duration=self._expansion_duration, ease=self._expansion_ease)
                self._redraw_background()
            return True

        elif event.type == pygame.MOUSEBUTTONDOWN: # Check if we pressed a mouse button
            if event.button == 1: # Left click input
                mouse_x, mouse_y = event.pos
                if button_hitbox.collidepoint(mouse_x, mouse_y): # Check if inside the button's region
                    self.is_pressed = True
                    self._redraw_background()
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed: # Left click release
                self.is_pressed = False # As long as the mouse is held down, the button will appear as if its
                # being pressed
                self._redraw_background()

                # Check if mouse is still over button to finish the click, if we move outside the button's region,
                # act as if the user did not mean to interact with the button
                mouse_x, mouse_y = event.pos
                if button_hitbox.collidepoint(mouse_x, mouse_y): # Check if inside button's region
                    if self.on_click: # If a click function exists, call it
                        self.on_click()
                    return True

        return False # Did not consume event

    def update(self, dt: float) -> None:
        """Update expansion animation if enabled."""
        # Update expansion tween and size
        if self.expand_on_hover:
            prev_progress = self._expand_tween.current
            progress = self._expand_tween.update(dt)
            if progress != prev_progress:
                self._current_width = self.base_width + (self.expanded_width - self.base_width) * progress
                # Keep visual expansion to the right (left and top stay the same) to keep no positional change
                self._redraw_background()

    def render(self, screen: pygame.Surface) -> None:
        """Render the button and its contents."""
        if not self.visible: # Do not render if the element is invisible
            return None

        # Keep the hit-rect aligned with the panel
        self.set_hitbox_rect((self.panel.x, self.panel.y, self.base_width, self.height))

        # Relayout text according to visual width
        self._layout_text()

        # Draw the panel
        self.panel.render(screen)
