
import os
from typing import Iterable
from random_parser.base_parser import BaseParser
from random_parser.constants import GENERATOR_IMPORT_KEYWORD, GENERATOR_PARSER, RESOURCE_IMPORT_KEYWORD, RESOURCE_PARSER
from random_parser.imports_cache import ImportsCache

class ImportsParser(BaseParser):
    """The ImportsParser parses imports."""

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, imports_cache: ImportsCache):
        super().__init__(filename, lines, line_num)
        self.imports_cache = imports_cache

    def parse(self, import_type: str, import_handle: str, import_filename: str):
        if import_handle in self.imports_cache.imports:
            return self

        assert import_type in [GENERATOR_IMPORT_KEYWORD, RESOURCE_IMPORT_KEYWORD], self.err_msg(f'Got invalid import_type "{import_type}"')
        if import_type == GENERATOR_IMPORT_KEYWORD:
            folder = self.imports_cache.generator_folder
        else:
            folder = self.imports_cache.resources_folder

        filepath = os.path.join(folder, import_filename)
        with open(filepath) as f:
            lines = f.read().split('\n')
            if import_type == GENERATOR_IMPORT_KEYWORD:
                parser = generator_parser.GeneratorParser(self.filename, lines, 0, self)
                parser_type =  GENERATOR_PARSER
            else:
                parser = resource_parser.ResourceParser(self.filename, lines, 0, self)
                parser_type =  RESOURCE_PARSER
            parser.parse()
            self.imports_cache.store(import_handle, parser_type, parser)
        
        return self

# Can't use "from x import y", or a circular dependency ensues.
import random_parser.resource_parser as resource_parser
import random_parser.generator_parser as generator_parser