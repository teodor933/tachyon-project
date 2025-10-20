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

        self._setup_title()
        self._setup_images()
        self._setup_buttons()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC to quit
                self.engine.set_is_running(False)

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self) -> None:
        self.engine.screen.fill((50, 50, 50))
        super().render()

    def on_enter(self, previous_scene: Optional["Scene"], data: Optional[Dict[str, Any]] = None) -> None:
        print(f"Entering Main Menu from {previous_scene.__class__.__name__ if previous_scene else 'startup'}")

    def _setup_title(self):
        title = Text(
            x=150,
            y=self.engine.screen.get_height() // 2 - 200,
            layer=1,
            text="Tachyon",
            font_size=100,
            colour=(255, 255, 255),
            centre_text=True
        )
        self.add_ui_element(title)

    def _setup_images(self):
        image = Image(
            x=self.engine.screen.get_width() // 2,
            y=self.engine.screen.get_height() // 2,
            layer=0,
            centre_image=True
        )
        self.add_ui_element(image)

    def _setup_buttons(self):

        base_x = 0
        base_y = 220
        width = 200
        expanded = 320
        height = 50
        gap = 18
        def add_main_button(caption: str, y: int, on_click):
            button = Button(
                x=base_x,
                y=y,
                width=width,
                height=height,
                on_click=on_click,
                text=caption,
                font_size=36,
                text_colour=(255, 255, 255),
                normal_colour=(25, 25, 25),
                hover_colour=(70, 70, 70),
                pressed_colour=(180, 180, 180),
                centre_text=True,
                centre_surface=False,
                layer=1,
                border_colour=(255, 255, 255),
                border_width=1,
                border_radius=0,
                hover_tint=None,
                padding=16,
                expand_on_hover=True,
                expanded_width=expanded,
                expansion_duration=0.18,
                expansion_ease="ease_out",
            )
            self.add_ui_element(button)
            return button

        def start_game():
            self.engine.scene_manager.change_scene("game")

        add_main_button("Play", base_y + 0 * (height + gap), start_game)

