import os

import yaml
from loguru import logger


DEV_MODE = os.getenv("DEV_MODE") == 1

with open("config.yaml") as file:
    config = yaml.full_load(file)


class YAMLGetter(type):
    """
    Implements a custom metaclass used for accessing
    configuration data by simply accessing class attributes.
    Supports getting configuration from up to two levels
    of nested configuration through `section` and `subsection`.
    `section` specifies the YAML configuration section (or "key")
    in which the configuration lives, and must be set.
    `subsection` is an optional attribute specifying the section
    within the section from which configuration should be loaded.
    Example Usage:
        # config.yml
        game:
            window:
                height: 200
                width: 200

        # config.py
        class Options(metaclass=YAMLGetter):
            section = "game"
            subsection = "window"

        # Usage in Python code
        from config import Options
        def get_size():
            return Options.width
    """

    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return config[cls.section][cls.subsection][name]
            return config[cls.section][name]
        except KeyError:
            path = '.'.join(
                (cls.section, cls.subsection, name)
                if cls.subsection is not None else (cls.section, name)
            )
            error_msg = f"Tried accessing configuration variable at `{path}`, but it could not be found."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def __getitem__(cls, name):
        return cls.__getattr__(name)


class Window(metaclass=YAMLGetter):
    section = "window"

    tick_rate: int
    height: int
    width: int


class Simulation(metaclass=YAMLGetter):
    section = "simulation"

    cube_scale: int
    projection_distance: int
    orthographic: bool
