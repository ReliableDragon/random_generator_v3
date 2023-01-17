

from typing import Dict, Union

from random_parser.imports_cache import ImportsCache

class Context():

    def __init__(self, imports_cache: ImportsCache, state: Dict[str, Union[str, int]]):
        self.imports_cache = imports_cache
        self.state = state

    def get_import(self, name):
        return self.imports_cache[name]