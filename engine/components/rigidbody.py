from dataclasses import dataclass, field
import pygame
from engine.ecs.component import Component
from engine.ecs.registry import register_component


@register_component("RigidBody")
@dataclass
class RigidBody(Component):
    mass: float = 1.0

    velocity: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0), metadata={"save": True})
    max_velocity: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(1000, 1000))
    acceleration: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0))

    gravity_scale: float = 1.0
    drag: float = 0.0 # air resistance
    is_kinematic: bool = False # not affected by forces while True

    def __post_init__(self):
        if not isinstance(self.velocity, pygame.Vector2):
            self.velocity = pygame.Vector2(self.velocity)
        if not isinstance(self.max_velocity, pygame.Vector2):
            self.max_velocity = pygame.Vector2(self.max_velocity)
        if not isinstance(self.acceleration, pygame.Vector2):
            self.acceleration = pygame.Vector2(self.acceleration)

    def add_force(self, force):
        """Adds a force to the body (F = ma, so a = F/m)"""
        if not self.is_kinematic:
            self.acceleration += force / self.mass

    def add_impulse(self, impulse):
        """Adds an instant velocity change (I = mv, so v = I/m)"""
        if not self.is_kinematic:
            self.velocity += impulse / self.mass