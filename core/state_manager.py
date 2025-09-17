from typing import List
import pygame


class GameStateManager:
    def __init__(self, game: "Game"):
        self.game = game
        self.stack: List["State"] = []

    def push(self, state: "State") -> None:
        self.stack.append(state)
        state.on_enter()

    def pop(self) -> None:
        if self.stack:
            self.stack[-1].on_exit()
            self.stack.pop()

    def change(self, new_state: "State") -> None:
        while self.stack:
            self.pop()
        self.push(new_state)

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        if self.stack:
            self.stack[-1].handle_events(events)

    def fixed_update(self, dt_fixed: float) -> None:
        if self.stack:
            self.stack[-1].fixed_update(dt_fixed)

    def update(self, dt: float) -> None:
        if self.stack:
            self.stack[-1].update(dt)

    def render(self, screen) -> None:
        for state in self.stack:
            state.render(screen)
