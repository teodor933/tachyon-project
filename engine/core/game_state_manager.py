import json
import os
import pygame

from engine.components.serialisable import Serialisable
from engine.components.transform import Transform


class GameStateManager:
    """Handles saving and loading the game state."""
    def __init__(self, world, save_path="save_game.json"):
        self.world = world
        self.save_path = save_path

    def save_game(self):
        """Saves the state of all serialisable entities."""
        save_data = {"entities": {}}

        serialisable_entities = self.world.get_entities_with(Serialisable, Transform)

        for entity in serialisable_entities:
            serialisable_component = entity.get_component(Serialisable)
            transform_component = entity.get_component(Transform)

            # only saving position for now, must expand later with health, etc
            entity_state = {
                "transform": {
                    "position": [transform_component.position.x, transform_component.position.y]
                }
            }
            save_data["entities"][serialisable_component.unique_id] = entity_state

        with open(self.save_path, "w") as f:
            json.dump(save_data, f, indent=2)
        print(f"Game state saved to {self.save_path}")

    def load_game(self):
        """Loads and applies the saved game state to the current world."""
        if not os.path.exists(self.save_path):
            print("No save file found.")
            return

        with open(self.save_path, "r") as f:
            save_data = json.load(f)

        serialisable_entities = self.world.get_entities_with(Serialisable, Transform)
        entity_map = {entity.get_component(Serialisable).unique_id: entity for entity in serialisable_entities}

        for unique_id, entity_state in save_data.get("entities", {}).items():
            entity = entity_map.get(unique_id)
            if entity:
                # apply the only transform state we have at the moment
                transform_state = entity_state.get("transform", {})
                if "position" in transform_state:
                    pos = transform_state["position"]
                    entity.get_component(Transform).position = pygame.Vector2(pos[0], pos[1])

        print(f"Game state loaded from {self.save_path}")

    def has_save_file(self):
        return os.path.exists(self.save_path)
