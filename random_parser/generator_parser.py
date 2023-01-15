
import logging
from typing import Iterable
from random_parser.base_parser import BaseParser

from random_parser.choice_body_parser import ChoiceBodyParser
from random_parser.utils import generate_err_msg


class GeneratorParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int):
        super().__init__(filename, lines, line_num)
        self.name = None
        self.body = None

    def parse_generator(self):
        assert self.lines, self.err_msg('Empty file provided')
        self.name = self.use_line()
        logging.info(f'Starting to parse generator "{self.name}".')

        assert self.use_line() == '', self.err_msg(
            'Generator did not contain a name and choice body separated by a newline')

        assert self.lines, self.err_msg('Generator did not contain a choice body')
        self.body = ChoiceBodyParser(self.filename, self.lines, self.line_num)
        self.body.parse()
        self.line_num = self.body.line_num

        return self

    def get_body(self):
        return self.body
