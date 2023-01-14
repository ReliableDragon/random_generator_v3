import os

from typing import IO, Iterable, Optional, TextIO

class Parser():
    """Parse files for random generation.

    Attrributes:
    generator_filter: Currently just a single generator name to match against,
    which will avoid compiling all the other generators if provided. In the future
    may be extended to include more features.
    generators_folder: Determines where to look for top-level generators.
    inputs_folder: Determines where to look for inputs."""

    generator_filter: str
    generators_folder: str
    inputs_folder: str

    def __init__(self, generators_folder: str = None,
                 inputs_folder: str = None):
        self.generators_folder = generators_folder if generators_folder else r'top_level_generators/'
        self.inputs_folder = inputs_folder if inputs_folder else r'inputs/'

    def parse(self, generator_filter: str = None):
        self.parse_top_level_generators(generator_filter)

    def parse_top_level_generators(self, generator_filter: Optional[str] = None) -> Iterable[str]:
        results = []
        for file in os.listdir(self.generators_folder):
            # Skip any generators that don't match the filter.
            if generator_filter:
                if file.split('.')[0] != generator_filter:
                    continue
            filepath = os.path.join(self.generator_folder, file)
            with open(filepath) as f:
                generator = self.parse_generator(f)
                results.append(generator)
        return results