from engine.core.game_state_manager import GameStateManager
from engine.core.resource_manager import ResourceManager
from engine.core.scene import Scene
from engine.core.scene_loader import SceneLoader
from engine.systems.physics_system import PhysicsSystem
from engine.systems.render_system import RenderSystem
from engine.systems.input_system import InputSystem
from engine.systems.animation_system import PlayerAnimationSystem


class GameLevel(Scene):
    """A scene that loads its content from data files."""
    def __init__(self, game_engine, level_path, load_save=False):
        super().__init__(game_engine)
        self.level_path = level_path
        self.load_save = load_save

    def on_enter(self):
        # core systems
        self.resources = ResourceManager()
        self.loader = SceneLoader(self.world, self.resources, "data/prefabs.json")
        self.state_manager = GameStateManager(self.world)

        # load level data and get scene settings
        scene_settings = self.loader.load_level(self.level_path)

        # add systems
        self.input_system = self.add_system(InputSystem())
        self.physics_system = self.add_system(PhysicsSystem(gravity=scene_settings.get("gravity", -980)))
        self.animation_system = self.add_system(PlayerAnimationSystem())
        self.render_system = self.add_system(RenderSystem(self.engine.screen, self.resources))

        if "background_color" in scene_settings:
            self.render_system.background_color = tuple(scene_settings["background_color"])

        # load saved game state if requested
        if self.load_save:
            self.state_manager.load_game()

    def on_exit(self):
        """Save the game state when exiting a scene."""
        self.state_manager.save_game()
        super().on_exit()