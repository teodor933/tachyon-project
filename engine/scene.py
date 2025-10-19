from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

import pygame.event

from engine.user_interface.ui_element import UIElement


class Scene(ABC):
    """Abstract base class for all scenes in the game."""
    def __init__(self, engine: "GameEngine"):
        """
        Initialise the scene.
        :param engine: Reference to the main game engine instance.
        """
        self.engine = engine
        self.ui_elements: list[UIElement] = [] # List of all required UI elements to be rendered on this screen

    def add_ui_element(self, element: UIElement):
        """Add a UI element to this scene."""
        self.ui_elements.append(element)

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Handle input events for this scene.
        :param events: List of Pygame events to process.
        """
        sorted_elements = sorted(self.ui_elements, key=lambda elem: elem.layer, reverse=True) # Sort elements in
        # descending order to handle the events of the top layers first

        for event in events:
            for element in sorted_elements:
                if element.handle_event(event): # Check if the UI element has successfully handled an input event
                    break # If handled an event type, do not allow other elements to handle the same event

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update scene game state.
        :param dt: Delta time in seconds since last frame.
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """Render the scene to the screen."""
        sorted_elements = sorted(self.ui_elements, key=lambda elem: elem.layer) # Sort elements in ascending order to
        # render the top layers last

        for element in sorted_elements:
            element.render(self.engine.screen)

    def on_enter(self, previous_scene: Optional["Scene"], data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when entering this scene.
        :param previous_scene: The scene we are transitioning from, or None if first scene.
        :param data: Optional dictionary containing data passed from the previous scene.
        """
        pass

    def on_exit(self, next_scene: "Scene") -> Optional[Dict[str, Any]]:
        """
        Called when leaving this scene.
        :param next_scene: The scene we are transitioning to.
        :return: Optional dictionary containing data to pass to the next scene.
        """
        return None