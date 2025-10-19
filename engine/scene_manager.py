from typing import Optional, Dict, Any

import pygame.event

from engine.scene import Scene
from engine.scene_registry import get_scene_class


class SceneManager:
    """Manages scene transitions and delegates control to the active scene."""
    def __init__(self, engine: "GameEngine"):
        """
        Initialise the scene manager.
        :param engine: Reference to the main game engine instance.
        """
        self.engine = engine
        self.current_scene: Optional[Scene] = None # Control variable for storing the current scene

    def change_scene(self, scene_name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Change to a different scene.
        :param scene_name: The name of the scene to switch to.
        :param data: Optional data to pass to the new scene.
        """
        scene_class = get_scene_class(scene_name) # Get scene class found in the scene_registry variable

        transition_data = data # Get transition data from what the current scene passed, if it exists
        previous_scene = self.current_scene # Store current scene as now the previous scene

        if self.current_scene:
            exit_data = self.current_scene.on_exit(scene_class) # Return any data from the on_exit method
            # if available

            if exit_data: # If we have data from on_exit, store it in the transition data dictionary
                transition_data = {**(exit_data or {}), **(data or {})} # Prioritise our manually passed data,
                # therefore, we override any exit_data key-values with passed data

        self.current_scene = scene_class(self.engine) # Set the current scene as an instance of the
        # gathered scene
        self.current_scene.on_enter(previous_scene, transition_data) # Call required code upon entering a new scene
        # and pass on data from the previous scene

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Delegate event handling to the current scene."""
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt: float) -> None:
        """Delegate update to the current scene."""
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self) -> None:
        """Delegate rendering to the current scene."""
        if self.current_scene:
            self.current_scene.render()



