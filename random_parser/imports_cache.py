
from typing import Iterable

class ImportsCache():
    """The ImportsParser is a SHARED parser that is used to cache all imported files."""

    def __init__(self, generator_folder: str, resources_folder: str):
        self.generator_folder = generator_folder
        self.resources_folder = resources_folder
        self.imports = {}