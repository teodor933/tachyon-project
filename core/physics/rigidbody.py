from dataclasses import dataclass
from pygame.math import Vector2

@dataclass
class RigidBody2D:
    mass: float = 1.0
    vel: Vector2 = Vector2(0, 0)
    force: Vector2 = Vector2(0, 0)
    gravity_scale: float = 1.0

    on_ground: bool = False
    in_air: bool = False
    has_jump: bool = False
    has_jumped: bool = False # fuck wait these dont go on rigidbodies do they
    # remove later
