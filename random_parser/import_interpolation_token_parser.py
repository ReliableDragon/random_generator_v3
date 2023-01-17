from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import GENERATOR_PARSER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER, RESOURCE_PARSER
from random_parser.context import Context

from random_parser.token_parser import TokenParser


class ImportInterpolationTokenParser(TokenParser):

    def __init__(self, parser: TokenParser, token_num: int):
        super().__init__(parser, token_num=token_num)
        self.import_handle = None

    def evaluate(self, context: Context):
        import_ = context.imports_cache.get(self.import_handle)
        if import_.parser_type == GENERATOR_PARSER:
            return import_.parser.evaluate(context)
        elif import_.parser_type == RESOURCE_PARSER:
            return import_.parser.evaluate(context)
        else:
            raise ValueError(f'Got unsupported parser type: {import_.parser_type}')

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
            # Don't consume following space
            while self.char() != IMPORT_ITPL_END:
                self.import_handle += self.use_char()
            return self