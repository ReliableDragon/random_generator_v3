import logging
from typing import Iterable
from random_parser.base_parser import BaseParser


# Abstract
class TokenParser(BaseParser):

    def __init__(self,
            token_parser: 'TokenParser' = None,
            base_parser: BaseParser = None,
            char_num: int = None,
            token_num: int = None):
        # Handle base class construction
        if token_parser:
            super().__init__(token_parser)
        elif base_parser:
            super().__init__(base_parser)
        else:
            raise ValueError('Must provide one of token_parser or base_parser!')
        # Set up new fields
        self.token_num = None
        self.char_num = None
        # Maybe import from token_parser
        if token_parser:
            self.token_num = token_parser.token_num
            self.char_num = token_parser.char_num
        # Allow explicitly set values to override inherited ones from a token_parser
        if token_num is not None:
            self.token_num = token_num
        if char_num is not None:
            self.char_num = char_num
        # Set defaults and validate
        if self.token_num is None:
            self.token_num = 1
        if self.char_num is None:
            raise ValueError('Must provide char_num, either through a token_parser or manually!')

    def char(self):
        try:
            return self.line()[self.char_num]
        except IndexError as e:
            logging.error(self.err_msg('Attempted to consume characters past end of line!'))
            raise e

    def use_char(self):
        char = self.char()
        self.char_num += 1
        return char

    def get_char_num(self):
        return self.char_num + 1

    def context(self):
        return self.line()[self.char_num:self.char_num+25]

    def sync(self, other):
        if isinstance(other, TokenParser):
            self.char_num = other.char_num
        self.line_num = other.line_num

    def is_eol(self):
        return self.char_num == len(self.line())

    def _msg_intro(self):
        return f'{self.__class__.__name__}, file {self.filename}, line {self.get_line_num()}, char {self.get_char_num()}, token #{self.token_num}>'