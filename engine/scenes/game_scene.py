from typing import Optional, Dict, Any

import pygame.event

from engine.scene import Scene
from engine.scene_registry import register_scene
from engine.user_interface.button import Button
from engine.user_interface.image import Image
from engine.user_interface.text import Text


@register_scene("game")
class GameScene(Scene):
    """Main Menu scene."""
    def __init__(self, engine: "GameEngine"):
        super().__init__(engine)

        self._setup_images()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC to pause
                self.engine.scene_manager.push_scene("pause_menu")

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self) -> None:
        self.engine.screen.fill((165, 185, 198))
        super().render()

    def on_enter(self, previous_scene: Optional["Scene"], data: Optional[Dict[str, Any]] = None) -> None:
        print(f"Entering Main Menu from {previous_scene.__class__.__name__ if previous_scene else 'startup'}")

    def _setup_images(self):
        image = Image(
            x=self.engine.screen.get_width() // 2,
            y=self.engine.screen.get_height() // 2,
            layer=0,
            centre_image=True
        )
        self.add_ui_element(image)

