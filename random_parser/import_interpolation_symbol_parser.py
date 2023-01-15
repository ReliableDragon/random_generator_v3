from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER

from random_parser.symbol_parser import SymbolParser


class ImportInterpolationSymbolParser(SymbolParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, expression: str, char_num: int):
        super().__init__(filename, lines, line_num, expression, char_num)
        self.import_handle = None

    def parse(self):
        logging.debug(f'IISP processing line {self.line()} at char #{self.char_num}: "{self.char()}"')
        assert self.char() == IMPORT_INTERPOLATION_MARKER, self.err_msg('Attempted to parse starting from invalid character!')
        self.use_char()

        self.import_handle = ''
        if self.char() == IMPORT_ITPL_OPEN_DELIMITER:
            self.use_char()
            while self.char() != IMPORT_ITPL_CLOSE_DELIMITER:
                self.import_handle += self.use_char()
            self.use_char()
            return self
        else:
            while self.char() != IMPORT_ITPL_END:
                self.import_handle += self.use_char()
            return self