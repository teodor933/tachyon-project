import pygame
from engine.core.scene import Scene
from engine.components.transform import Transform
from engine.components.sprite import Sprite
from engine.components.rigidbody import RigidBody
from engine.components.collider import BoxCollider
from engine.components.player_controller import PlayerController
from engine.systems.physics_system import PhysicsSystem
from engine.systems.render_system import RenderSystem
from engine.systems.input_system import InputSystem
from engine.systems.animation_system import PlayerAnimationSystem


class TestLevel(Scene):
    def on_enter(self):
        # set up the level
        # added systems in the order they should execute
        self.add_system(InputSystem())
        self.add_system(PhysicsSystem(gravity=-9.8 * 150)) # adjust later
        self.add_system(PlayerAnimationSystem(stretch_factor=0.3, squish_factor=0.3))
        self.add_system(RenderSystem(self.engine.screen))

        # create player
        self.create_player(400, 300)

        # create temp ground platforms
        self.create_ground()

        # create some temp floating platforms
        self.create_platform(200, 400, 150, 20)
        self.create_platform(500, 350, 150, 20)
        self.create_platform(700, 450, 100, 20)
        self.create_platform(300, 250, 100, 20)

        # create some walls
        self.create_wall(50, 360, 20, 200)
        self.create_wall(750, 360, 20, 200)

    def create_player(self, x, y):
        """Create the player entity"""
        player = self.world.create_entity()

        # create a coloured rectangle for the player sprite
        player_surface = pygame.Surface((32, 32))
        player_surface.fill((255, 100, 100)) # roughly red

        player.add_component(Transform(pygame.Vector2(x, y)))
        player.add_component(Sprite(player_surface, layer=10))
        player.add_component(RigidBody(
            mass=1.0,
            gravity_scale=1.0,
            drag=0.05,
            max_velocity=pygame.Vector2(800, 1600)
        ))
        player.add_component(BoxCollider(
            width=32,
            height=32,
            is_static=False
        ))
        player.add_component(PlayerController(
            move_speed=300,
            jump_force=650,
            max_jumps=2,
            acceleration=2000,
            friction=15,
            air_control=1
        ))

        # transform, sprite, rigidbody, boxCollider, playerController

        return player

    def create_ground(self):
        ground = self.world.create_entity()

        ground_surface = pygame.Surface((1200, 40))
        ground_surface.fill((100, 200, 100))  # green

        ground.add_component(Transform(pygame.Vector2(1280/2, 580)))
        ground.add_component(Sprite(ground_surface, layer=0))
        ground.add_component(BoxCollider(
            width=1200,
            height=40,
            is_static=True
        ))

        return ground

    def create_platform(self, x, y, width, height):
        platform = self.world.create_entity()

        platform_surface = pygame.Surface((width, height))
        platform_surface.fill((150, 150, 150))  # grey

        platform.add_component(Transform(pygame.Vector2(x, y)))
        platform.add_component(Sprite(platform_surface, layer=1))
        platform.add_component(BoxCollider(
            width=width,
            height=height,
            is_static=True
        ))

        return platform

    def create_wall(self, x, y, width, height):
        wall = self.world.create_entity()

        wall_surface = pygame.Surface((width, height))
        wall_surface.fill((80, 80, 80))  # dark grey

        wall.add_component(Transform(pygame.Vector2(x, y)))
        wall.add_component(Sprite(wall_surface, layer=1))
        wall.add_component(BoxCollider(
            width=width,
            height=height,
            is_static=True
        ))

        return wall