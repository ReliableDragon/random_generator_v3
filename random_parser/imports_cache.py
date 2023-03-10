
from dataclasses import dataclass
from typing import Iterable, Union, TYPE_CHECKING


class ImportsCache():
    """The ImportsParser is a SHARED parser that is used to cache all imported files."""

    @dataclass
    class Import():
        import_handle: str
        parser_type: str
        parser: Union['generator.GeneratorParser', 'resource.ResourceParser']

    def __init__(self, generator_folder: str, resources_folder: str):
        self.generator_folder = generator_folder
        self.resources_folder = resources_folder
        self.imports = {}

    def store(self, import_handle, parser_type, parser):
        self.imports[import_handle] = self.Import(import_handle, parser_type, parser)

    def get(self, import_handle):
        return self.imports[import_handle]

    def list_imports(self):
        return [i.import_handle for i in self.imports.values()]

if TYPE_CHECKING:
    import random_parser.generator as generator
    import random_parser.resource as resource