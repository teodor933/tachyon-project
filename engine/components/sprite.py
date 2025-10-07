from dataclasses import dataclass
from engine.ecs.component import Component
from engine.ecs.registry import register_component


@register_component("Sprite")
@dataclass
class Sprite(Component):
    """
    Holds information for rendering an entity.
    The pygame.Surface is retrieved from the ResourceManager with asset_id.
    """
    asset_id: str
    layer: int = 0
    visible: bool = True
    flip_x: bool = False
    flip_y: bool = False
    colour: tuple = (255, 255, 255)
    alpha: int = 255