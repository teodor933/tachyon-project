from dataclasses import dataclass
from engine.ecs.component import Component


@dataclass
class Serialisable(Component):
    """
    A marker component for entities whose state should be saved.
    """
    unique_id: str = None