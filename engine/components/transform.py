from dataclasses import dataclass, field
import pygame
from engine.ecs.component import Component

@dataclass
class Transform(Component):
    position: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0))
    rotation: float = 0.0 # floats are immutable, no need for field()
    scale: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(1, 1))

    def __post_init__(self):
        if not isinstance(self.position, pygame.Vector2):
            self.position = pygame.Vector2(self.position)
        if not isinstance(self.scale, pygame.Vector2):
            self.scale = pygame.Vector2(self.scale)