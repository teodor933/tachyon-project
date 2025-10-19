from typing import Optional, Dict, Any

import pygame.event

from engine.scene import Scene
from engine.scene_registry import register_scene
from engine.user_interface.button import Button
from engine.user_interface.image import Image
from engine.user_interface.text import Text


@register_scene("main_menu")
class MainMenuScene(Scene):
    """Main Menu scene."""
    def __init__(self, engine: "GameEngine"):
        super().__init__(engine)
        image = Image(
            x=engine.screen.get_width() // 2,
            y=engine.screen.get_height() // 2,
            layer=0,
            centre_image=True
        )  # Create image
        self.add_ui_element(image)

        title = Text(
            x=engine.screen.get_width() // 2,
            y=engine.screen.get_height() // 2 - 200,
            layer=1,
            text="Tachyon",
            font_size=100,
            colour=(255, 255, 255),
            centre_text=True
        ) # Create title text
        self.add_ui_element(title)

        play_button = Button(
            x=engine.screen.get_width() // 2,
            y=engine.screen.get_height() // 2,
            width=200,
            height=50,
            text="Play",
            font_size=36,
            text_colour=(255, 255, 255),
            normal_colour=(50, 150, 50),
            hover_colour=(70, 200, 70),
            pressed_colour=(30, 100, 30),
            centre_surface=True,
            centre_text=False,
            layer=1,
            on_click=self.start_game
        )
        self.add_ui_element(play_button)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super().handle_events(events)

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self) -> None:
        self.engine.screen.fill((255, 0, 0))
        super().render()

    def on_enter(self, previous_scene: Optional["Scene"], data: Optional[Dict[str, Any]] = None) -> None:
        print(f"Entering Main Menu from {previous_scene.__class__.__name__ if previous_scene else "startup"}")

    def start_game(self):
        """Callback for the Play button."""
        print("Starting game...")