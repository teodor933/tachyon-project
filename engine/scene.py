"""
Abstract base class for all game scenes.

Scenes manage their own UI elements, event handling, updates, and rendering.
This class enforces a consistent interface across all scenes.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable
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
        """
        Add a UI element to this scene.
        :param element: The UI element to add.
        :return: The added element.
        """
        self.ui_elements.append(element)
        return element

    def remove_ui_element(self, element: UIElement):
        """
        Remove a UI element from this scene.
        :param element: The UI element to remove.
        """
        if element in self.ui_elements:
            self.ui_elements.remove(element)

    def clear_ui_elements(self):
        """Remove all UI elements from the scene."""
        self.ui_elements.clear()

    def find_ui_element(self, predicate: Callable[[UIElement], bool]) -> Optional[UIElement]:
        """
        Find the first UI element matching a condition.
        :param predicate: Function to test each element.
        :return: First matching element, or None if not found.
        """
        for element in self.ui_elements:
            if predicate(element):
                return element
        return None

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Handle input events for this scene.

        Processes events in descending layer order.
        Stops propagation once an event is handled.
        :param events: List of Pygame events to process.
        """
        sorted_elements = sorted(self.ui_elements, key=lambda elem: elem.layer, reverse=True) # Sort elements in
        # descending order to handle the events of the top layers first

        for event in events:
            for element in sorted_elements:
                if not element.enabled: # Skip over this element
                    continue
                if element.handle_event(event): # Check if the UI element has successfully handled an input event
                    break # If handled an event type, stop the propagation

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update the scene's logic and UI elements.
        :param dt: Delta time in seconds since last frame.
        """
        for element in self.ui_elements:
            element.update(dt)

    @abstractmethod
    def render(self) -> None:
        """
        Render the scene and its UI elements.

        Renders elements in ascending layer order.
        """
        sorted_elements = sorted(self.ui_elements, key=lambda elem: elem.layer) # Sort elements in ascending order to
        # render the top layers last

        for element in sorted_elements:
            element.render(self.engine.screen)

    def on_enter(self, previous_scene: Optional["Scene"], data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when entering this scene.

        Override to initialise state or load data.
        :param previous_scene: Scene being transitioned from.
        :param data: Optional dictionary containing data passed from the previous scene.
        """
        pass

    def on_exit(self, next_scene: "Scene") -> Optional[Dict[str, Any]]:
        """
        Called when leaving this scene.

        Override to return data to the next scene.
        :param next_scene: Scene being transitioned to.
        :return: Optional dictionary containing data to pass forward to the next scene.
        """
        return None

    def on_resume(self, previous_top: Optional["Scene"]) -> None:
        """
        Called when this scene becomes active again after being paused.
        :param previous_top: The scene that was popped.
        """
        pass
