from dataclasses import dataclass
import pygame
from engine.ecs.component import Component

@dataclass
class BoxCollider(Component):
    width: float
    height: float
    offset: pygame.Vector2 = None # offset from the transform position
    is_trigger: bool = False # detects collisions only
    is_static: bool = False # does not move, like platforms

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