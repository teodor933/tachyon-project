import pygame
from dataclasses import is_dataclass, fields

_type_adapters = {
    pygame.Vector2: {
        "encode": lambda v: [v.x, v.y],
        "decode": lambda l: pygame.Vector2(l)
    }
}

def encode_component(instance, for_save_game=False):
    """
    Converts a component instance to a dictionary.
    If for_save_game is True, only includes fields marked with "save".
    """
    if not is_dataclass(instance):
        return instance

    data = {}
    for field in fields(instance):
        if for_save_game and not field.metadata.get("save", False):
            continue

        value = getattr(instance, field.name)
        encoder = _type_adapters.get(type(value), {}).get("encode")

        if encoder:
            data[field.name] = encoder(value)
        elif is_dataclass(value):
            data[field.name] = encode_component(value, for_save_game)
        else:
            data[field.name] = value

    return data

def decode_component(component_class, data):
    """Creates a component instance from a dictionary."""
    if not is_dataclass(component_class):
        raise TypeError("Class must be a dataclass to be decoded.")

    key_args = {}
    for field in fields(component_class):
        if field.name not in data:
            continue

        field_value = data[field.name]
        decoder = _type_adapters.get(field.type, {}).get("decode")

        if decoder and isinstance(field_value, list):
            key_args[field.name] = decoder(field_value)
        elif is_dataclass(field.type) and isinstance(field_value, dict):
            key_args[field.name] = decode_component(field.type, field_value)
        else:
            key_args[field.name] = field_value

    return component_class(**key_args)
