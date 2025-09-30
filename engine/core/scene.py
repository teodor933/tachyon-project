from engine.ecs.world import World


class Scene:
    """Base class for all game scenes"""
    def __init__(self, game_engine):
        self.engine = game_engine
        self.world = World()
        self.systems = []

    def add_system(self, system):
        """Add a system to the scene"""
        self.systems.append(system)
        system.on_enter()
        return system

    def remove_system(self, system):
        """Remove a system from the scene"""
        if system in self.systems:
            system.on_exit()
            self.systems.remove(system)

    def update(self, dt):
        """Update all systems"""
        for system in self.systems:
            if system.enabled:
                system.update(self.world, dt)

        # clean up destroyed entities
        self.world.process_destruction()

    def on_enter(self):
        """Called when scene becomes active"""
        pass

    def on_exit(self):
        """Called when scene becomes inactive"""
        for system in self.systems:
            system.on_exit()
