import pygame.key

from engine.components.player_controller import PlayerController
from engine.components.rigidbody import RigidBody
from engine.components.sprite import Sprite
from engine.systems.base import System


class InputSystem(System):
    """Handles player input"""
    def __init__(self):
        super().__init__()

    def update(self, world, dt):
        keys = pygame.key.get_pressed()

        for entity in world.get_entities_with(PlayerController, RigidBody):
            controller = entity.get_component(PlayerController)
            rb = entity.get_component(RigidBody)
            sprite = entity.get_component(Sprite)

            # horizontal movement
            move_x = 0
            if keys[pygame.K_a]:
                move_x = -1
                controller.facing_right = False
                if sprite:
                    sprite.flip_x = True

            if keys[pygame.K_d]:
                move_x = 1
                controller.facing_right = True
                if sprite:
                    sprite.flip_x = False

            # apply movement
            if move_x != 0:
                if controller.is_grounded:
                    rb.add_force(pygame.Vector2(move_x * controller.acceleration, 0))
                else:
                    # in air
                    rb.add_force(pygame.Vector2(move_x * controller.acceleration * controller.air_control, 0))
            elif controller.is_grounded:
                # add temporary friction to slow down to zero
                rb.velocity.x *= (1 - controller.friction * dt)

            # jumping
            if keys[pygame.K_SPACE]:
                if hasattr(controller, "_jump_pressed"):
                    if not controller._jump_pressed and controller.jumps_remaining > 0:
                        rb.velocity.y = -controller.jump_force
                        controller.jumps_remaining -= 1
                        controller._jump_pressed = True
                else:
                    controller._jump_pressed = True
            else:
                controller._jump_pressed = False
