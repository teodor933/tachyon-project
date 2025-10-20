"""
Manages scene transitions using a stack-based system.

The SceneManager handles pushing, popping, and replacing scenes,
delegating events, updates, and rendering to the active scenes.
"""

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
        self._stack: list[Scene] = []

    @property
    def current_scene(self) -> Optional[Scene]:
        """
        Get the currently active scene (top of the stack).
        :return: The top scene, or None if the stack is empty.
        """
        return self._stack[-1] if self._stack else None # Top of the stack

    def change_scene(self, scene_name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Replace all scenes with a new one.

        Clears the entire scene stack and pushes the specified scene.
        :param scene_name: Name of the scene to activate.
        :param data: Optional data to pass to the new scene.
        """
        # Exit all current scenes
        self._stack.clear()

        self.push_scene(scene_name, data)

    def push_scene(self, scene_name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Push a new scene onto the stack.

        The new scene becomes active, and the previous scene is paused.
        :param scene_name: The name of the scene to push.
        :param data: Optional data to pass to the new scene.
        """
        scene_class = get_scene_class(scene_name)
        previous_scene = self.current_scene
        new_scene = scene_class(self.engine)
        self._stack.append(new_scene)
        new_scene.on_enter(previous_scene, data)

    def pop_scene(self) -> None:
        """
        Remove the top scene and resume the one beneath it.

        If the stack becomes empty, nothing happens.
        """
        if not self._stack:
            return None
        popped = self._stack.pop()
        next_top = self.current_scene
        if next_top:
            next_top.on_resume(popped)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Delegate event handling to the current scene.
        :param events: List of events to process.
        """
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt: float) -> None:
        """
        Delegate update to the current scene.
        :param dt: Delta time in seconds since the last frame.
        """
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self) -> None:
        """Delegate rendering to the current scene in stack order."""
        for scene in self._stack:
            scene.render()
