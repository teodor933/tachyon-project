from dataclasses import dataclass
from engine.ecs.component import Component

@dataclass
class PlayerController(Component):
    move_speed: float = 300.0
    jump_force: float = 600.0
    max_jumps: int = 2
    jumps_remaining: int = 2
    acceleration: float = 1000.0 # how quickly should the player accelerate, different to rigidbody acceleration
    friction: float = 10.0 # ground friction
    air_control: float = 0.3

    is_grounded: bool = False
    facing_right: bool = True