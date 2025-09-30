import pygame

from engine.components.sprite import Sprite
from engine.components.transform import Transform
from engine.systems.base import System

class RenderSystem(System):
    """Handles rendering of all sprites"""
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.camera_offset = pygame.Vector2(0, 0)

    def update(self, world, dt):
        self.screen.fill((255, 255, 255))

        renderables = world.get_entities_with(Sprite, Transform)

        renderables.sort(key=lambda e: e.get_component(Sprite).layer) # render by layer defined

        for entity in renderables:
            sprite = entity.get_component(Sprite)
            transform = entity.get_component(Transform)

            if not sprite.visible:
                continue

            image = sprite.image

            # apply new scale if needed
            if transform.scale != (1, 1):
                size = (int(image.get_width() * transform.scale.x),
                        int(image.get_height() * transform.scale.y))
                image = pygame.transform.scale(image, size)

            # apply rotations
            if transform.rotation != 0:
                image = pygame.transform.rotate(image, transform.rotation)

            # apply flips
            if sprite.flip_x or sprite.flip_y:
                image = pygame.transform.flip(image, sprite.flip_x, sprite.flip_y)

            # apply alpha
            if sprite.alpha < 255:
                image.set_alpha(sprite.alpha)

            # calculate render position
            rect = image.get_rect()
            rect.center = transform.position - self.camera_offset

            self.screen.blit(image, rect)