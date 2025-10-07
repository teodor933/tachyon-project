from dataclasses import dataclass
from engine.ecs.component import Component
from engine.ecs.registry import register_component


@register_component("Serialisable")
@dataclass
class Serialisable(Component):
    """
    A marker component for entities whose state should be saved.
    """
    unique_id: str = None