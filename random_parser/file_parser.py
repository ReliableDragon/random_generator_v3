from __future__ import annotations

import logging
from typing import Iterable, TYPE_CHECKING
from random_parser.base_parser import BaseParser
from random_parser.imports_cache import ImportsCache

from random_parser.utils import generate_err_msg


class FileParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, imports_cache: ImportsCache):
        super().__init__(filename, lines, line_num)
        self.name = None
        self.imports_cache = imports_cache

    def maybe_parse_imports(self):
        parsed_imports = False
        while self.line().startswith('generator') or self.line().startswith('resource'):
            import_type, import_data = self.use_line().split(' ')
            import_handle, import_filename = import_data.split(':')
            imports_parser = ImportsParser(import_filename, self.lines, self.line_num, self.imports_cache)
            imports_parser.parse(import_type, import_handle, import_filename)
            # Do not update line_num based on imports, as they are a different file.
            parsed_imports = True

        if parsed_imports:
            assert self.line() == '', self.err_msg(
                'Generator did not contain a blank line after imports')
            self.use_line()


    def parse_header(self):
        assert self.lines, self.err_msg('Empty file provided')
        self.name = self.use_line()
        logging.info(f'Starting to parse generator "{self.name}".')

        assert self.line() == '', self.err_msg(
            'Generator did not contain a blank line after name')
        self.use_line()

        assert self.line(), self.err_msg('Expected populated line')
        self.maybe_parse_imports()

        assert self.lines, self.err_msg('Generator did not contain any content after the header')

        return self

    def parse(self):
        self.parse_header()

from random_parser.imports_parser import ImportsParser