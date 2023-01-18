from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.context import Context

from random_parser.file_parser import FileParser
from random_parser.imports_cache import ImportsCache
from random_parser.interpolation_blocks.interpolation_block import InterpolationBlockParser


class ResourceParser(FileParser):

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, imports_cache: ImportsCache):
        super().__init__(filename, lines, line_num, imports_cache)
        self.interpolation_block = None

    def evaluate(self, context: Context):
        return self.interpolation_block.evaluate(context)

    def parse(self):
        super().parse()

        assert self.lines, self.err_msg('Generator did not contain an interpolation block')
        self.interpolation_block = InterpolationBlockParser(self)
        self.interpolation_block.parse()
        self.sync(self.interpolation_block)

        return self