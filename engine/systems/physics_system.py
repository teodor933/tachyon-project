import pygame

from engine.components.collider import BoxCollider
from engine.components.player_controller import PlayerController
from engine.components.rigidbody import RigidBody
from engine.components.transform import Transform
from engine.systems.base import System


class PhysicsSystem(System):
    """Handles physics simulation"""
    def __init__(self, gravity=-9.8):
        super().__init__()
        self.gravity = pygame.Vector2(0, -gravity)

    def update(self, world, dt):
        # apply physics calculations to entities
        # entities with a rigidbody and transform only
        for entity in world.get_entities_with(RigidBody, Transform):
            rb = entity.get_component(RigidBody)
            transform = entity.get_component(Transform)

            if not rb.is_kinematic:
                rb.add_force(self.gravity * rb.mass * rb.gravity_scale) # weight = mass * gravitational field strength

                if rb.drag > 0:
                    rb.velocity *= (1 - rb.drag * dt) # as drag is increased, velocity is decreased

                rb.velocity += rb.acceleration * dt # a = v - u / t -> v = u + at

                # -max < v < +max
                rb.velocity.x = max(-rb.max_velocity.x, min(rb.velocity.x, rb.max_velocity.x))
                rb.velocity.y = max(-rb.max_velocity.y, min(rb.velocity.y, rb.max_velocity.y))

                transform.position += rb.velocity * dt # s = 0.5 * (v + u)t -> vt

                rb.acceleration = pygame.Vector2(0, 0) # reset acceleration for next frame to avoid large accumulations
                # to improve later

        self.handle_collisions(world)

    def handle_collisions(self, world):
        dynamic_entities = world.get_entities_with(RigidBody, Transform, BoxCollider)
        static_entities = world.get_entities_with(Transform, BoxCollider)

        for dynamic in dynamic_entities:
            d_transform = dynamic.get_component(Transform)
            d_collider = dynamic.get_component(BoxCollider)
            d_rb = dynamic.get_component(RigidBody)

            if d_collider.is_static or d_rb.is_kinematic:
                continue

            d_rect = d_collider.get_rect(d_transform.position)

            # check if on ground for player controller
            player_controller = dynamic.get_component(PlayerController)
            if player_controller:
                player_controller.is_grounded = False

            for static in static_entities:
                if static == dynamic:
                    continue

                s_transform = static.get_component(Transform)
                s_collider = static.get_component(BoxCollider)
                s_rect = s_collider.get_rect(s_transform.position)

                if d_rect.colliderect(s_rect) and not d_collider.is_trigger and not s_collider.is_trigger:
                    # simple collision correction to make sure objects are not on top of each other
                    # if collided, check how far right we are to the left of the static object and vice versa
                    overlap_x = min(d_rect.right - s_rect.left, s_rect.right - d_rect.left)
                    # if collided, check how far down we are into the top of the static object and vice versa
                    overlap_y = min(d_rect.bottom - s_rect.top, s_rect.bottom - d_rect.top)

                    if overlap_x < overlap_y:
                        # horizontal collision
                        if d_rect.centerx < s_rect.centerx:
                            d_transform.position.x -= overlap_x
                            d_rb.velocity.x = min(d_rb.velocity.x, 0)
                        else:
                            d_transform.position.x += overlap_x
                            d_rb.velocity.x = max(d_rb.velocity.x, 0)
                    else:
                        # vertical collision
                        if d_rect.centery < s_rect.centery: # d is above s
                            d_transform.position.y -= overlap_y
                            d_rb.velocity.y = min(d_rb.velocity.y, 0)

                            # entity is on an object, grounded
                            if player_controller and d_rb.velocity.y <= 0:
                                player_controller.is_grounded = True
                                player_controller.jumps_remaining = player_controller.max_jumps
                        else:
                            d_transform.position.y += overlap_y # d is below s
                            d_rb.velocity.y = max(d_rb.velocity.y, 0)
