from abc import ABC, abstractmethod

from engine.ecs.registry import SystemPhase


class System(ABC):
    """Base class for all systems"""

    def __init__(self):
        self.enabled = True
        self.phase = SystemPhase.UPDATE # default phase

    @classmethod
    def from_config(cls, config, **kwargs):
        """Create a system instance from a configuration dictionary."""
        return cls()

    @abstractmethod
    def update(self, world, dt):
        """Update the system with delta time in seconds."""
        pass

    def on_enter(self, world):
        """Called when system is added to scene."""
        pass

    def on_exit(self):
        """Called when system is removed from scene."""
        pass
