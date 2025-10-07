import json

import pygame

from engine.components.tags import Tags
from engine.components.transform import Transform
from engine.components.sprite import Sprite
from engine.components.rigidbody import RigidBody
from engine.components.collider import BoxCollider, PhysicsMaterial
from engine.components.player_controller import PlayerController
from engine.components.serialisable import Serialisable
from engine.core.resource_manager import ResourceManager
from engine.ecs.world import World


class SceneLoader:
    """Handles loading scenes and entities from JSON files."""

    COMPONENT_MAP = {
        "Transform": Transform,
        "Sprite": Sprite,
        "RigidBody": RigidBody,
        "BoxCollider": BoxCollider,
        "PlayerController": PlayerController,
        "Serialisable": Serialisable,
        "Tags": Tags,
    }

    def __init__(self, world, resource_manager, prefabs_path):
        self.world: World = world
        self.resource_manager: ResourceManager = resource_manager
        with open(prefabs_path, "r") as f:
            self.prefabs = json.load(f)

    def create_component(self, component_name, data):
        """Creates a component instance from JSON data."""
        component_class = self.COMPONENT_MAP.get(component_name)
        if not component_class:
            raise ValueError(f"Unknown component type: {component_name}")

        # handle the nested dictionary in data structures like PhysicsMaterial
        if "material" in data and isinstance(data["material"], dict):
            data["material"] = PhysicsMaterial(**data["material"])

        # convert appropriate lists to pygame vectors
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 2:
                data[key] = pygame.Vector2(value)

        return component_class(**data)

    def load_level(self, level_path):
        """Loads a full level, including assets and entities."""
        with open(level_path, "r") as f:
            level_data = json.load(f)

        self.resource_manager.load_assets_from_json(level_path)

        for entity_data in level_data.get("entities", []):
            self.create_entity_from_data(entity_data)

        return level_data

    def create_entity_from_data(self, entity_data):
        """Creates a single entity from a prefab and override data."""
        prefab_name = entity_data.get("prefab")
        if not prefab_name:
            raise ValueError("Entity data must contain a prefab key.")

        prefab = self.prefabs.get(prefab_name)
        if not prefab:
            raise ValueError(f"Prefab {prefab_name} not found.")

        entity = self.world.create_entity()

        for component_name, component_data in prefab.get("components", {}).items():
            # copy to avoid modifying the prefab base
            data = component_data.copy()

            overrides = entity_data.get("overrides", {}).get(component_name, {})
            data.update(overrides)

            component = self.create_component(component_name, data)
            entity.add_component(component)

        if prefab.get("save_on_quit"):
            unique_id = entity_data.get("name", f"{prefab_name}_{entity.id}")
            entity.add_component(Serialisable(unique_id=unique_id))

        return entity
