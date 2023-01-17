from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable

from random_parser.file_parser import FileParser
from random_parser.imports_cache import ImportsCache
from random_parser.choice_block import ChoiceBlockParser


class GeneratorParser(FileParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, imports_cache: ImportsCache):
        super().__init__(filename, lines, line_num, imports_cache)
        self.choice_block = None

    def evaluate(self, context):
        logging.debug(f'Evaluating...')
        return self.choice_block.evaluate(context)

    def parse(self):
        super().parse()

        assert self.lines, self.err_msg('Generator did not contain an choice block')
        self.choice_block = ChoiceBlockParser(self)
        self.choice_block.parse()
        self.sync(self.choice_block)

        return self