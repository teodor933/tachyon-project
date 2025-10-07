from engine.core.event_bus import EventBus
from engine.core.game_state_manager import GameStateManager
from engine.core.resource_manager import ResourceManager
from engine.core.scene import Scene
from engine.core.scene_loader import SceneLoader
from engine.ecs.registry import get_system_info
from engine.systems.physics_system import PhysicsSystem
from engine.systems.render_system import RenderSystem
from engine.systems.animation_system import PlayerAnimationSystem
from engine.systems.input_actions_system import InputActionsSystem
from engine.systems.player_control_system import PlayerControlSystem


class GameLevel(Scene):
    """A scene that loads its content from data files."""
    def __init__(self, game_engine, level_path, load_save=False):
        super().__init__(game_engine)
        self.level_path = level_path
        self.load_save = load_save

    def on_enter(self):
        # core systems
        self.resources = ResourceManager()
        self.state_manager = GameStateManager(self.world)
        self.event_bus = EventBus()
        self.world.add_resource("event_bus", self.event_bus)

        # load level data and get scene settings
        self.loader = SceneLoader(self.world, self.resources, "data/prefabs.json")
        level_data = self.loader.load_level(self.level_path)
        scene_settings = level_data.get("scene_settings", {})

        for system_data in level_data.get("systems", []):
            system_name = system_data["type"]
            system_config = system_data.get("config", {})

            system_info = get_system_info(system_name)
            system_class = system_info["class"]

            # create system instacnes from the config
            system_instance = system_class.from_config(
                system_config,
                engine=self.engine,
                world=self.world,
                resource_manager=self.resources
            )
            system_instance.phase = system_info["phase"]
            self.add_system(system_instance)

        # load saved game state if requested
        if self.load_save:
            self.state_manager.load_game()

    def on_exit(self):
        """Save the game state when exiting a scene."""
        self.state_manager.save_game()
        super().on_exit()