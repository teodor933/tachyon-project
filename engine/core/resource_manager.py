import pygame
import json


class ResourceManager:
    """A manager for loading game assets."""
    def __init__(self):
        self.assets = {}

    def load_assets_from_json(self, file_path):
        """Loads multiple assets defined in a JSON file."""
        with open(file_path, "r") as f:
            asset_definitions = json.load(f)

        for asset_id, definition in asset_definitions.get("assets", {}).items():
            self.load_asset(asset_id, definition)

    def load_asset(self, asset_id, definition):
        """Loads a single asset based on its definition."""
        if asset_id in self.assets:
            return

        asset_type = definition.get("type")
        if asset_type == "image":
            self.assets[asset_id] = pygame.image.load(definition["path"]).convert_alpha()
        elif asset_type == "font":
            self.assets[asset_id] = pygame.font.Font(definition.get("path"), definition["size"])
        elif asset_type == "surface":
            size = tuple(definition["size"])
            colour = tuple(definition["colour"])
            surface = pygame.Surface(size)
            surface.fill(colour)
            self.assets[asset_id] = surface

    def get_asset(self, asset_id):
        """Retrieves a loaded asset."""
        return self.assets.get(asset_id)

    def clear(self):
        """Clears all loaded assets."""
        self.assets.clear()