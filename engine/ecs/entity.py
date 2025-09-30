class Entity:
    """An entity is a container for components with a unique ID"""
    def __init__(self, world, entity_id):
        self.world = world
        self.id = entity_id
        self.components = {}
        self.active = True

    def add_component(self, component):
        component_type = type(component)
        self.components[component_type] = component
        self.world.register_component(self, component_type)
        return self

    def remove_component(self, component_type):
        if component_type in self.components:
            del self.components[component_type]
            self.world.unregister_component(self, component_type)

    def get_component(self, component_type):
        return self.components.get(component_type)

    def has_component(self, *component_types):
        return all(comp in self.components for comp in component_types)

    def destroy(self):
        self.active = False
        self.world.destroy_entity(self)
