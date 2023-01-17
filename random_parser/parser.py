import logging
import os

from random_parser.generator_parser import GeneratorParser

from typing import IO, Iterable, Optional, TextIO
from random_parser.imports_cache import ImportsCache

from random_parser.imports_parser import ImportsParser

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
    resources_folder: str

    top_level_generators: Iterable[GeneratorParser]

    def __init__(self, generators_folder: str = None,
                 resources_folder: str = None):
        self.generators_folder = generators_folder if generators_folder else r'generators/'
        self.resources_folder = resources_folder if resources_folder else r'generators/resources/'
        self.imports_cache = ImportsCache(self.generators_folder, self.resources_folder)

    def parse(self, generator_filter: str = None) -> None:
        self.parse_top_level_generators(generator_filter)

    def parse_generator(self, f: TextIO, filename: str, lines: Iterable[str]) -> str:
        generator_parser = GeneratorParser(filename, lines, 0, self.imports_cache)
        parsed_file = generator_parser.parse()
        return parsed_file

    def parse_top_level_generators(self, generator_filter: Optional[str] = None) -> None:
        self.top_level_generators = []
        for filename in os.listdir(self.generators_folder):
            # Skip any generators that don't match the filter.
            if generator_filter:
                if generator_filter not in filename:
                    continue

            filepath = os.path.join(self.generators_folder, filename)
            # Skip non-file objects, such as folders.
            if not os.path.isfile(filepath):
                continue
            logging.info(f'Opening generator file {filepath}.')
            with open(filepath) as f:
                lines = f.read().split('\n')
                # Remove comments
                lines = [line.split(';')[0] for line in lines]
                generator = self.parse_generator(f, filename, lines)
                self.top_level_generators.append(generator)
