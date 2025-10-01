import math
import pygame

from engine.components.collider import BoxCollider, PhysicsMaterial
from engine.components.player_controller import PlayerController
from engine.components.rigidbody import RigidBody
from engine.components.transform import Transform
from engine.systems.base import System

def combine_restitution(a: PhysicsMaterial, b: PhysicsMaterial) -> float:
    # max of the two
    return max(a.restitution, b.restitution)

def combine_friction(a: PhysicsMaterial, b: PhysicsMaterial):
    mu_s = math.sqrt(a.static_friction * b.static_friction)
    mu_d = math.sqrt(a.dynamic_friction * b.dynamic_friction)
    return mu_s, mu_d


class PhysicsSystem(System):
    """Handles physics simulation"""
    def __init__(self, gravity=-9.8, solver_iterations=8, baumgarte=0.8, slop=0.01, restitution_velocity_threshold=1.0):
        super().__init__()
        self.gravity = pygame.Vector2(0, -gravity)
        self.solver_iterations = solver_iterations
        self.baumgarte = baumgarte  # % of penetration to solve per step with position correction
        self.slop = slop  # small penetration tolerated before we try a correction pass
        self.restitution_velocity_threshold = restitution_velocity_threshold # limit bounces on objects

    def update(self, world, dt):
        bodies = world.get_entities_with(RigidBody, Transform)

        # reset grounded state for all controllers, to manually set through contacts
        for entity in world.get_entities_with(PlayerController):
            controller = entity.get_component(PlayerController)
            print(entity.get_component(RigidBody).velocity)
            print(controller.is_grounded)
            controller.is_grounded = False

        # apply physics calculations to entities
        # entities with a rigidbody and transform only
        for entity in bodies:
            rb = entity.get_component(RigidBody)
            transform = entity.get_component(Transform)

            if rb.is_kinematic: # if not affected by forces, skip
                rb.acceleration = pygame.Vector2(0, 0)
                continue

            # external forces
            rb.add_force(self.gravity * rb.mass * rb.gravity_scale) # weight = mass * gravitational field strength

            rb.velocity += rb.acceleration * dt # a = v - u / t -> v = u + at

            if rb.drag > 0:
                rb.velocity *= (1 - rb.drag * dt)  # as drag is increased, velocity is decreased

            # -max < v < +max
            rb.velocity.x = max(-rb.max_velocity.x, min(rb.velocity.x, rb.max_velocity.x))
            rb.velocity.y = max(-rb.max_velocity.y, min(rb.velocity.y, rb.max_velocity.y))

            transform.position += rb.velocity * dt  # s = 0.5 * (v + u)t -> vt

            rb.acceleration = pygame.Vector2(0, 0)  # reset acceleration for next frame to avoid large accumulations

        # detect contacts
        contacts = self._build_contacts(world)

        for _ in range(self.solver_iterations):
            # in case an object A is resolved from hitting object B,
            # but now they hit another object C, so another pass is needed
            for contact in contacts:
                self._solve_contact_velocity(contact, dt)

        for contact in contacts: # in case impulse correction has not worked fully
            self._position_correction(contact)

        self._update_grounded_flags(contacts, world)

    @staticmethod
    def _is_static(entity, collider: BoxCollider):
        rb = entity.get_component(RigidBody)
        if collider.is_static:
            return True
        if rb is None:
            return True
        if rb.is_kinematic:
            return True
        return False

    def _build_contacts(self, world):
        colliders = world.get_entities_with(Transform, BoxCollider)
        contacts = []

        for i in range(len(colliders)):
            entity_a = colliders[i]
            a_tr = entity_a.get_component(Transform)
            a_col = entity_a.get_component(BoxCollider)

            if a_col.is_trigger:
                continue

            for j in range(i + 1, len(colliders)):
                entity_b = colliders[j]
                b_tr = entity_b.get_component(Transform)
                b_col = entity_b.get_component(BoxCollider)

                if b_col.is_trigger:
                    continue

                # half extents of colliders
                a_he = a_col.half_extents()
                b_he = b_col.half_extents()

                # centres of colliders
                a_centre = pygame.Vector2(a_tr.position.x + a_col.offset.x, a_tr.position.y + a_col.offset.y)
                b_centre = pygame.Vector2(b_tr.position.x + b_col.offset.x, b_tr.position.y + b_col.offset.y)

                dx = b_centre.x - a_centre.x
                overlap_x = (a_he.x + b_he.x) - abs(dx)
                if overlap_x <= 0: # if current x distance is greater than the min distance, no collision
                    continue

                dy = b_centre.y - a_centre.y
                overlap_y = (a_he.y + b_he.y) - abs(dy)
                if overlap_y <= 0: # if current y distance is greater than the min distance, no collision
                    continue

                if overlap_x < overlap_y:
                    normal_x = 1.0 if dx > 0 else -1.0
                    normal = pygame.Vector2(normal_x, 0.0)
                    penetration = overlap_x
                else:
                    normal_y = 1.0 if dy > 0 else -1.0
                    normal = pygame.Vector2(0.0, normal_y)
                    penetration = overlap_y

                contacts.append(Contact(entity_a, entity_b, normal, penetration))

        return contacts

    def _solve_contact_velocity(self, contact, dt):
        entity_a = contact.entity_a
        entity_b = contact.entity_b
        normal = contact.normal # a to b

        a_rb = entity_a.get_component(RigidBody)
        b_rb = entity_b.get_component(RigidBody)
        a_col = entity_a.get_component(BoxCollider)
        b_col = entity_b.get_component(BoxCollider)

        a_static = self._is_static(entity_a, a_col)
        b_static = self._is_static(entity_b, b_col)

        inv_ma = 0.0 if a_static else (0.0 if a_rb is None or a_rb.mass == 0 else 1.0 / a_rb.mass)
        inv_mb = 0.0 if b_static else (0.0 if b_rb is None or b_rb.mass == 0 else 1.0 / b_rb.mass)

        inv_mass_sum = inv_ma + inv_mb
        if inv_mass_sum == 0:
            return

        va = a_rb.velocity if a_rb is not None else pygame.Vector2(0, 0)
        vb = b_rb.velocity if b_rb is not None else pygame.Vector2(0, 0)

        relative_velocity = vb - va # a to b
        vel_along_normal = relative_velocity.dot(normal) # relative velocity dot normal vector

        # if separate, skip normal impulse for now, objects are moving away from each other
        if vel_along_normal > 0:
            return

        restitution = combine_restitution(a_col.material, b_col.material)
        if abs(vel_along_normal) < self.restitution_velocity_threshold:
            restitution = 0.0

        # normal impulse
        impulse_magnitude = -(1 + restitution) * vel_along_normal
        impulse_magnitude /= inv_mass_sum

        impulse = normal * impulse_magnitude
        # J = Ft => Ft = mv-mu therefore, mv-mu / m = v-u
        # v = u + J/m
        if a_rb is not None and not a_static:
            a_rb.velocity -= impulse * inv_ma
        if b_rb is not None and not b_static:
            b_rb.velocity += impulse * inv_mb

        # friction impulse
        tangent = relative_velocity - (relative_velocity.dot(normal)) * normal
        t_len_sq = tangent.x * tangent.x + tangent.y * tangent.y
        if t_len_sq > 1e-12:
            t = tangent.normalize()
            vt = relative_velocity.dot(t)

            tangent_impulse_magnitude = -vt
            tangent_impulse_magnitude /= inv_mass_sum

            static_friction, dynamic_friction = combine_friction(a_col.material, b_col.material)
            # clamp friction, static first, then kinetic
            if abs(tangent_impulse_magnitude) <= impulse_magnitude * static_friction:
                friction_impulse = t * tangent_impulse_magnitude
            else:
                friction_impulse = t * (-impulse_magnitude * dynamic_friction * math.copysign(1.0, vt))

            if a_rb is not None and not a_static:
                a_rb.velocity -= friction_impulse * inv_ma
            if b_rb is not None and not b_static:
                b_rb.velocity += friction_impulse * inv_mb

    def _position_correction(self, contact):
        a = contact.entity_a
        b = contact.entity_b
        n = contact.normal

        a_tr = a.get_component(Transform)
        b_tr = b.get_component(Transform)
        a_rb = a.get_component(RigidBody)
        b_rb = b.get_component(RigidBody)
        a_col = a.get_component(BoxCollider)
        b_col = b.get_component(BoxCollider)

        a_static = self._is_static(a, a_col)
        b_static = self._is_static(b, b_col)

        inv_ma = 0.0 if a_static else (0.0 if a_rb is None or a_rb.mass == 0 else 1.0 / a_rb.mass)
        inv_mb = 0.0 if b_static else (0.0 if b_rb is None or b_rb.mass == 0 else 1.0 / b_rb.mass)
        inv_mass_sum = inv_ma + inv_mb
        if inv_mass_sum == 0:
            return

        correction_mag = max(contact.penetration - self.slop, 0.0) * self.baumgarte / inv_mass_sum
        correction = n * correction_mag

        if not a_static:
            a_tr.position -= correction * inv_ma
        if not b_static:
            b_tr.position += correction * inv_mb

    def _update_grounded_flags(self, contacts, world):
        grounded_by_entity = {}

        for contact in contacts:
            # A side
            a = contact.entity_a
            a_rb = a.get_component(RigidBody)
            if a_rb is not None:
                nA = -contact.normal
                if nA.y < -0.5 and a_rb.velocity.y >= 0:
                    grounded_by_entity[a.id] = True
            # B side
            b = contact.entity_b
            b_rb = b.get_component(RigidBody)
            if b_rb is not None:
                nB = contact.normal
                if nB.y < -0.5 and b_rb.velocity.y >= 0:
                    grounded_by_entity[b.id] = True

        # apply to any player controllers on the entities
        for entity_id, grounded in grounded_by_entity.items():
            entity = world.entities.get(entity_id)
            if entity is None:
                continue
            player = entity.get_component(PlayerController)
            if player:
                player.is_grounded = True
                player.jumps_remaining = player.max_jumps

class Contact:
    # dunder slots instead of dunder dict, to improve speed and memory usage
    __slots__ = ("entity_a", "entity_b", "normal", "penetration")

    def __init__(self, entity_a, entity_b, normal, penetration):
        self.entity_a = entity_a # entity 1
        self.entity_b = entity_b # entity 2
        self.normal = normal # normal vector
        self.penetration = penetration