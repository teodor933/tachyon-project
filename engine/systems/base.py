from abc import ABC, abstractmethod


class System(ABC):
    """Base class for all systems"""

    def __init__(self):
        self.enabled = True

    @abstractmethod
    def update(self, world, dt):
        """Update the system with delta time in seconds"""
        pass

    def on_enter(self):
        """Called when system is added to scene"""
        pass

    def on_exit(self):
        """Called when system is removed from scene"""
        pass
