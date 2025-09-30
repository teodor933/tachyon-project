from dataclasses import dataclass
import pygame
from engine.ecs.component import Component

@dataclass
class Sprite(Component):
    image: pygame.Surface # rectangular block of pixels
    layer: int = 0
    visible: bool = True
    flip_x: bool = False
    flip_y: bool = False
    colour: tuple = (255, 255, 255)
    alpha: int = 255

    @property
    def rect(self): # sprite.rect
        return self.image.get_rect() # get rectangular object for the surface