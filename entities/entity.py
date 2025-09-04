from typing import TypeVar
from dataclasses import dataclass

from pygame import Vector2


class Component:
    pass

T = TypeVar("T", bound=Component)

@dataclass
class RigidBody2D(Component):
    mass: float = 1.0

@dataclass
class Transform2D(Component):
    position: Vector2 = Vector2(0.0, 0.0)

class Entity:
    def __init__(self):
        pass

    def