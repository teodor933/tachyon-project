from typing import Dict, TypeVar, Optional
from dataclasses import dataclass
from pygame.math import Vector2

class Component:
    pass

T = TypeVar("T", bound=Component) # type variable that can only be a Component or subclass of it

@dataclass
class Transform(Component):
    pos: Vector2

class EntityFactory:
    def __init__(self):
        self._next_id = 0

    def create(self, name: str):
        entity = Entity(entity_id=self._next_id, name=name)
        self._next_id += 1
        return entity

class Entity:
    def __init__(self, entity_id: int, name: str = ""):
        self.id = entity_id
        self.name = name
        self.components: Dict[type, Component] = {}

    def add(self, component: Component):
        self.components[type(component)] = component
        return self

    def get(self) -> Optional[T]:
        raise NotImplementedError