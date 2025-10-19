"""Central scene registry for the game engine."""
from typing import Dict

_scene_registry: Dict[str, type] = {} # Global scene registry

def register_scene(name: str):
    """Decorator to automatically register a scene class."""
    def decorator(cls):
        _scene_registry[name] = cls
        return cls
    return decorator

def get_scene_class(name: str) -> type:
    """
    Get a registered scene class by name.
    :param name: The scene name to request.
    :return: The scene class in scene_registry.
    """
    if name not in _scene_registry:
        raise ValueError(f"Scene {name} is not registered.")
    return _scene_registry[name]

