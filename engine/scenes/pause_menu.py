from typing import Optional, Dict, Any

import pygame

from engine.scene import Scene
from engine.scene_registry import register_scene
from engine.user_interface.button import Button
from engine.user_interface.panel import Panel
from engine.user_interface.text import Text


@register_scene("pause_menu")
class PauseMenuScene(Scene):
    """Pause Menu overlay with left-anchored expanding buttons."""
    def __init__(self, engine: "GameEngine"):
        super().__init__(engine)

        self._setup_overlay()
        self._setup_title()
        self._setup_buttons()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC to resume
                self.engine.scene_manager.pop_scene()

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self) -> None:
        # Don't clear with fill(). Render on top of game
        super().render()

    def on_enter(self, previous_scene: Optional["Scene"], data: Optional[Dict[str, Any]] = None) -> None:
        print("Pause menu opened")

    def _setup_overlay(self):
        """Creates the semi-transparent background overlay."""
        self.overlay = Panel(
            x=0,
            y=0,
            width=self.engine.screen.get_width(),
            height=self.engine.screen.get_height(),
            bg_colour=(0, 0, 0),
            alpha=120,
            layer=0
        )
        self.add_ui_element(self.overlay)

    def _setup_title(self):
        title = Text(
            x=120,
            y=120,
            text="Paused",
            font_size=72,
            colour=(255, 255, 255),
            centre_text=True,
            layer=1
        )
        self.add_ui_element(title)

    def _setup_buttons(self):
        base_x = 0
        base_y = 220
        width = 128
        expanded = 320
        height = 64
        gap = 18
        def add_pause_button(caption: str, y: int, on_click):
            btn = Button(
                x=base_x,
                y=y,
                width=width,
                height=height,
                on_click=on_click,
                text=caption,
                font_size=28,
                text_colour=(255, 255, 255),
                normal_colour=(60, 60, 80),
                hover_colour=(90, 90, 130),
                pressed_colour=(50, 50, 70),
                centre_text=True,
                centre_surface=False,
                layer=2,
                border_colour=(255, 255, 255),
                border_width=1,
                border_radius=0,
                hover_tint=(43, 251, 238),
                padding=16,
                expand_on_hover=True,
                expanded_width=expanded,
                expansion_duration=0.18,
                expansion_ease="ease_out",
            )
            self.add_ui_element(btn)
            return btn

        def resume():
            # Pop pause menu and resume underlying scene
            self.engine.scene_manager.pop_scene()

        def settings():
            print("Settings clicked")

        def quit_to_menu():
            self.engine.scene_manager.change_scene("main_menu")

        add_pause_button("Resume", base_y + 0 * (height + gap), resume)
        add_pause_button("Settings", base_y + 1 * (height + gap), settings)
        add_pause_button("Quit to Menu", base_y + 2 * (height + gap), quit_to_menu)


