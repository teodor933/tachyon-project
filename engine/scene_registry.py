"""
Central registry for managing and retrieving game scenes.

This module provides a global dictionary that maps scene names to their corresponding classes,
enabling dynamic scene loading via decorators.
"""
from typing import Dict

# Global dictionary storing registered scene classes by name
_scene_registry: Dict[str, type] = {}

def register_scene(name: str):
    """
    Decorator to register a scene class under a given name.
    :param name: The unique identifier for the scene.
    :return: A decorator function that registers the class.
    """
    def decorator(cls):
        _scene_registry[name] = cls
        return cls
    return decorator

def get_scene_class(name: str) -> type:
    """
    Retrieve a registered scene class by its name.
    :param name: The name of the scene to retrieve.
    :return: The corresponding scene class.
    :raises ValueError: If the scene name is not registered.
    """
    if name not in _scene_registry:
        raise ValueError(f"Scene {name} is not registered.")
    return _scene_registry[name]
