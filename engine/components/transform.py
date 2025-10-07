from dataclasses import dataclass, field
import pygame
from engine.ecs.component import Component
from engine.ecs.registry import register_component


@register_component("Transform")
@dataclass
class Transform(Component):
    position: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0), metadata={"save": True})
    rotation: float = field(default=0.0, metadata={"save": True})
    scale: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(1, 1), metadata={"save": True})

    def __post_init__(self):
        if not isinstance(self.position, pygame.Vector2):
            self.position = pygame.Vector2(self.position)
        if not isinstance(self.scale, pygame.Vector2):
            self.scale = pygame.Vector2(self.scale)