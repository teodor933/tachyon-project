from enum import Enum, auto

_component_registry = {}
_system_registry = {}

class SystemPhase(Enum):
    INPUT = auto()
    UPDATE = auto()
    PHYSICS = auto()
    POST_PHYSICS = auto()
    ANIMATION = auto()
    RENDER = auto()
    UI = auto()


def register_component(name):
    """Decorator to register a component class with a given name."""
    def decorator(cls):
        _component_registry[name] = cls
        return cls
    return decorator

def register_system(name, phase=SystemPhase.UPDATE):
    """Decorator to register a system class with a given name and execution phase."""
    def decorator(cls):
        _system_registry[name] = {"class": cls, "phase": phase}
        return cls
    return decorator

def get_component_class(name):
    """Retrieves a component class from the registry."""
    cls = _component_registry.get(name)
    if not cls:
        raise ValueError(f"Component type {name} not found in registry.")
    return cls

def get_system_info(name):
    """Retrieves system information from the registry."""
    info = _system_registry.get(name) # class and phase in a dictionary
    if not info:
        raise ValueError(f"System type {name} not found in registry.")
    return info