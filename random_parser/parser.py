import os

from random_parser.generator_parser import GeneratorParser

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

    top_level_generators: Iterable[GeneratorParser]

    def __init__(self, generators_folder: str = None,
                 inputs_folder: str = None):
        self.generators_folder = generators_folder if generators_folder else r'top_level_generators/'
        self.inputs_folder = inputs_folder if inputs_folder else r'inputs/'

    def parse(self, generator_filter: str = None) -> None:
        self.parse_top_level_generators(generator_filter)

    def parse_generator(self, f: TextIO, filepath: str, filename: str) -> str:
        lines = f.read().split('\n')
        generator_parser = GeneratorParser(filename, lines, 0)
        parsed_file = generator_parser.parse_generator()
        return parsed_file

    def parse_top_level_generators(self, generator_filter: Optional[str] = None) -> None:
        self.top_level_generators = []
        for filename in os.listdir(self.generators_folder):
            # Skip any generators that don't match the filter.
            if generator_filter:
                if filename.split('.')[0] != generator_filter:
                    continue

            filepath = os.path.join(self.generators_folder, filename)
            with open(filepath) as f:
                generator = self.parse_generator(f, filepath, filename)
                self.top_level_generators.append(generator)
