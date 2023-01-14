import os

from typing import IO, Iterable, Optional, TextIO

from ..parser import Parser

class RandomGenerator():
    """Generates randomness!

    Attrributes:
    parser: The parser containing all the information about the parsed text files."""

    parser: Parser

    def __init__(self, parser: Parser):
        self.parser = parser

    # TODO: Implement.
    def parse_generator(self, f: TextIO(IO[str])) -> str:
        return f

    # TODO: Implement.
    def get_available_generations() -> Iterable[str]:
        return ['one', 'two', 'three']

    # TODO: Implement.
    def generate(choice: int = 0) -> str:
        return "Generation!"

    def list_top_level_generators(self, generator_filter: Optional[str] = None) -> Iterable[str]:
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