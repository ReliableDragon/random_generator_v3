import logging
from typing import Iterable
from random_parser.base_parser import BaseParser

class TokenParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, expression: str, char_num: int, token_num: int):
        super().__init__(filename, lines, line_num)
        self.expression = expression
        self.char_num = char_num
        self.token_num = token_num

    def char(self):
        try:
            return self.expression[self.char_num]
        except IndexError as e:
            logging.error(self.err_msg('Attempted to consume characters past end of line!'))
            raise e

    def use_char(self):
        char = self.char()
        self.char_num += 1
        return char

    def get_char_num(self):
        return self.char_num + 1