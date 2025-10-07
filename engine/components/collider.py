from dataclasses import dataclass, field
import pygame
from engine.ecs.component import Component
from engine.ecs.registry import register_component


@dataclass
class PhysicsMaterial(Component):
    static_friction: float = 0.6
    dynamic_friction: float = 0.5
    restitution: float = 0.0 # 0 = no bounce, 1 = perfectly elastic


@register_component("BoxCollider")
@dataclass
class BoxCollider(Component):
    width: float
    height: float
    offset: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0)) # offset from the transform position
    is_trigger: bool = False # detects collisions only
    is_static: bool = False # does not move, like platforms, infinite mass
    material: PhysicsMaterial = field(default_factory=PhysicsMaterial)
    layer: int = 1
    mask: int = -1 # collide with all layers by default

    def __post_init__(self):
        if self.offset is None:
            self.offset = pygame.Vector2(0, 0)
        elif not isinstance(self.offset, pygame.Vector2):
            self.offset = pygame.Vector2(self.offset)

    def get_rect(self, position):
        return pygame.Rect(
            position.x + self.offset.x - self.width/2,
            position.y + self.offset.y - self.height/2,
            self.width,
            self.height
        ) # (x, y) for rect objects is the top-left position, where x increases to the right and y increases downwards

    def half_extents(self) -> pygame.Vector2:
        return pygame.Vector2(self.width * 0.5, self.height * 0.5)