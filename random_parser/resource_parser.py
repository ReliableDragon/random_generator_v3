from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.base_parser import BaseParser

from random_parser.file_parser import FileParser
from random_parser.imports_cache import ImportsCache
from random_parser.interpolation_block_parser import InterpolationBlockParser
from random_parser.utils import generate_err_msg


class ResourceParser(FileParser):

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, imports_cache: ImportsCache):
        super().__init__(filename, lines, line_num, imports_cache)
        self.interpolation_block = None

    def parse(self):
        super().parse()

        assert self.lines, self.err_msg('Generator did not contain an interpolation block')
        self.interpolation_block = InterpolationBlockParser(self.filename, self.lines, self.line_num)
        self.interpolation_block.parse()
        self.line_num = self.interpolation_block.line_num

        return self