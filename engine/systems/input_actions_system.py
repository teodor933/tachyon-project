import json

import pygame

from engine.ecs.registry import register_system, SystemPhase
from engine.systems.base import System


@register_system("InputActionsSystem", phase=SystemPhase.INPUT)
class InputActionsSystem(System):

    @classmethod
    def from_config(cls, config, **kwargs):
        return cls(config["map_path"])

    def __init__(self, map_path):
        super().__init__()
        self.action_map = self.load_action_map(map_path)
        self.action_state = {}
        self.prev_keys = pygame.key.get_pressed()

    def load_action_map(self, map_path):
        with open(map_path, "r") as f:
            data = json.load(f)

        key_map = {}
        for action, keys in data["actions"].items(): # str, list
            pygame_keys = []
            for key in keys:
                if len(key) == 1 and key.isalpha():
                    pygame_key = getattr(pygame, f"K_{key.lower()}") # K_a, K_d, ...
                else:
                    pygame_key = getattr(pygame, f"K_{key.upper()}") # K_SPACE, ...
                pygame_keys.append(pygame_key)
            key_map[action] = pygame_keys
        return key_map

    def on_enter(self, world):
        """Share the action state with the world's resources."""
        world.add_resource("action_state", self.action_state)

    def update(self, world, dt):
        current_keys = pygame.key.get_pressed()

        for action, keys in self.action_map.items():
            pressed = any(current_keys[key] for key in keys)
            prev_pressed = any(self.prev_keys[key] for key in keys)

            self.action_state[action] = {
                "pressed": pressed,
                "just_pressed": pressed and not prev_pressed,
                "just_released": not pressed and prev_pressed
            }

        self.prev_keys = current_keys

