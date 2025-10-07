from dataclasses import dataclass, field

from engine.ecs.component import Component
from engine.ecs.registry import register_component


@register_component("Tags")
@dataclass
class Tags(Component):
    """A list of string tags for an entity."""
    values: list[str] = field(default_factory=list)