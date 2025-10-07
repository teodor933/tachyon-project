from engine.ecs.registry import SystemPhase
from engine.ecs.world import World


class Scene:
    """Base class for all game scenes"""
    def __init__(self, game_engine):
        self.engine = game_engine
        self.world = World()
        self.systems = []
        # 0: input, 1: update, 2: physics, 3: post_physics, 4: animation, 5: render, 6: ui
        self._phase_order = [
            SystemPhase.INPUT, SystemPhase.UPDATE, SystemPhase.PHYSICS,
            SystemPhase.POST_PHYSICS, SystemPhase.ANIMATION, SystemPhase.RENDER, SystemPhase.UI
        ]

    def add_system(self, system):
        """Add a system to the scene"""
        self.systems.append(system)
        self.systems.sort(key=lambda s: self._phase_order.index(s.phase))
        system.on_enter(self.world)
        return system

    def remove_system(self, system):
        """Remove a system from the scene"""
        if system in self.systems:
            system.on_exit()
            self.systems.remove(system)

    def update(self, dt):
        """Update all systems on a variable timestep"""
        for system in self.systems:
            if system.enabled and system.phase in [SystemPhase.ANIMATION, SystemPhase.RENDER, SystemPhase.UI]: # 4, 5 ,6
                system.update(self.world, dt)

        # clean up destroyed entities
        self.world.process_destruction()

    def fixed_update(self, dt):
        """Update all systems on a fixed timestep"""
        for system in self.systems:
            if system.enabled and system.phase in [SystemPhase.INPUT, SystemPhase.UPDATE,
                                                   SystemPhase.PHYSICS, SystemPhase.POST_PHYSICS]: # 0, 1, 2, 3
                system.update(self.world, dt)

    def on_enter(self):
        """Called when scene becomes active"""
        pass

    def on_exit(self):
        """Called when scene becomes inactive"""
        for system in self.systems:
            system.on_exit()
