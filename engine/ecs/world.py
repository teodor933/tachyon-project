from collections import defaultdict

from engine.ecs.entity import Entity


class World:
    """Container for all entities, components, and shared resources."""
    def __init__(self):
        self.entities = {}
        self.next_entity_id = 0
        self.entities_to_destroy = []
        self.component_index = defaultdict(set) # component type each has a set of entities
        self.resources = {}

    def add_resource(self, name, resource):
        """Adds a shared resource to the world."""
        self.resources[name] = resource

    def get_resource(self, name):
        """Retrieves a shared resource from the world."""
        return self.resources.get(name)

    def create_entity(self):
        """Create an entity."""
        entity = Entity(self, self.next_entity_id)
        self.entities[self.next_entity_id] = entity
        self.next_entity_id += 1
        return entity

    def destroy_entity(self, entity):
        """Mark entity for deletion (removed at end of frame)."""
        if entity not in self.entities_to_destroy:
            self.entities_to_destroy.append(entity)

    def register_component(self, entity, component_type):
        """Register that an entity has a component."""
        self.component_index[component_type].add(entity)

    def unregister_component(self, entity, component_type):
        """Unregister that an entity has a component."""
        self.component_index[component_type].discard(entity)

    def get_entities_with(self, *component_types):
        """Get all entities that have all specified components."""
        if not component_types:
            return []

        # Start with the set of entities that have the first component type, let this be set A
        # Copy in case we accidentally mutate the original index
        entities = self.component_index.get(component_types[0], set()).copy()

        # For every remaining component type (B, C, D...)
        # We update entities = entities union set_of_entities_with(component_type) : union operator -> &
        # Keep only entities that appear in all parsed sets
        for component_type in component_types[1:]:
            entities &= self.component_index.get(component_type, set())

        return [e for e in entities if e.active]

    def get_entity_with(self, *component_types):
        """Get first entity with specified components."""
        entities = self.get_entities_with(*component_types)
        return entities[0] if entities else None

    def process_destruction(self):
        """Remove all entities marked for destruction."""
        for entity in self.entities_to_destroy:
            if entity.id in self.entities:

                for component_type in entity.components.keys():
                    self.component_index[component_type].discard(entity)

                del self.entities[entity.id]
        self.entities_to_destroy.clear()
