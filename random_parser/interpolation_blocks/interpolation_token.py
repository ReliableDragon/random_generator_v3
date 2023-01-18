from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import INTERPOLATION_MARKER
from random_parser.token_parser import TokenParser


class InterpolationTokenParser(TokenParser):

    def parse(self):
        logging.debug(f'ITP processing line {self.line()} at char #{self.get_char_num()}: "{self.char()}"')
        assert self.char() == INTERPOLATION_MARKER, self.err_msg(f'Attempted to parse starting from invalid character "{self.char()}" (character {self.get_char_num()})')
        self.use_char()

        return self