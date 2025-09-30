import pygame
from engine.systems.base import System
from engine.components.player_controller import PlayerController
from engine.components.rigidbody import RigidBody
from engine.components.transform import Transform

class PlayerAnimationSystem(System):
    """Handles visual effects for the player, like squashing and stretching."""

    def __init__(self, stretch_factor=0.2, squish_factor=0.2):
        super().__init__()
        self.stretch_factor = stretch_factor
        self.squish_factor = squish_factor
        self.target_scale = pygame.Vector2(1, 1)

    def update(self, world, dt):
        player = world.get_entity_with(PlayerController, RigidBody, Transform)
        if not player:
            return

        controller = player.get_component(PlayerController)
        rb = player.get_component(RigidBody)
        transform = player.get_component(Transform)

        # reset scale when grounded
        if controller.is_grounded:
            self.target_scale = pygame.Vector2(1, 1)
        else:
            # in air
            if rb.velocity.y < 0:  # upwards
                # stretch vertically, squish horizontally
                self.target_scale.x = 1 - self.stretch_factor
                self.target_scale.y = 1 + self.stretch_factor
            elif rb.velocity.y > 0: # downwards
                # less extreme stretch while falling
                self.target_scale.x = 1 - self.stretch_factor / 2
                self.target_scale.y = 1 + self.stretch_factor / 2

        # Linearly interpolate the current scale towards the target scale
        current_scale = transform.scale
        transform.scale = current_scale.lerp(self.target_scale, 15 * dt)
