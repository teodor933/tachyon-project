import pygame

from engine.components.collider import BoxCollider
from engine.components.sprite import Sprite
from engine.components.transform import Transform
from engine.ecs.registry import register_system, SystemPhase
from engine.systems.base import System

@register_system("RenderSystem", phase=SystemPhase.RENDER)
class RenderSystem(System):
    """Handles rendering of all sprites using a ResourceManager."""

    @classmethod
    def from_config(cls, config, engine=None, resource_manager=None, **kwargs):
        return cls(engine.screen, resource_manager, config.get("background_color", (255, 255, 255)))

    def __init__(self, screen, resource_manager, background_color=(255, 255, 255)):
        super().__init__()
        self.screen = screen
        self.resource_manager = resource_manager
        self.camera_offset = pygame.Vector2(0, 0)
        self.background_color = background_color

    def update(self, world, dt):
        self.screen.fill(self.background_color)

        renderables = world.get_entities_with(Sprite, Transform)

        renderables.sort(key=lambda e: e.get_component(Sprite).layer) # render by layer defined

        for entity in renderables:
            sprite = entity.get_component(Sprite)
            transform = entity.get_component(Transform)

            if not sprite.visible:
                continue

            image = self.resource_manager.get_asset(sprite.asset_id)
            if not image:
                continue

            # copy to avoid modifying the saved asset
            image = image.copy()

            collider = entity.get_component(BoxCollider)  # Changed from string to class
            if collider and image.get_width() == 1 and image.get_height() == 1:
                size = (int(collider.width * transform.scale.x), int(collider.height * transform.scale.y))
                image = pygame.transform.scale(image, size)

            # apply new scale if needed
            elif transform.scale != (1, 1):
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