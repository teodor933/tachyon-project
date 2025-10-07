import pygame

from engine.components.player_controller import PlayerController
from engine.components.rigidbody import RigidBody
from engine.components.sprite import Sprite
from engine.ecs.registry import register_system, SystemPhase
from engine.systems.base import System


@register_system("PlayerControlSystem", phase=SystemPhase.UPDATE)
class PlayerControlSystem(System):
    """Handles player movement based on abstract input actions."""

    @classmethod
    def from_config(cls, config, **kwargs):
        return cls()

    def update(self, world, dt):
        action_state = world.get_resource("action_state")
        if not action_state:
            return

        for entity in world.get_entities_with(PlayerController, RigidBody):
            controller = entity.get_component(PlayerController)
            rb = entity.get_component(RigidBody)
            sprite = entity.get_component(Sprite)

            # horizontal movement
            move_x = 0
            if action_state.get("move_left", {}).get("pressed"):
                move_x = -1
                controller.facing_right = False
                if sprite:
                    sprite.flip_x = True

            if action_state.get("move_right", {}).get("pressed"):
                move_x = 1
                controller.facing_right = True
                if sprite:
                    sprite.flip_x = False

            # apply movement
            if move_x != 0:
                force_multiplier = 1.0 if controller.is_grounded else controller.air_control
                rb.add_force(pygame.Vector2(move_x * controller.acceleration * force_multiplier, 0))

            if action_state.get("jump", {}).get("just_pressed"):
                if controller.jumps_remaining > 0:
                    rb.velocity.y = -controller.jump_force
                    controller.jumps_remaining -= 1
