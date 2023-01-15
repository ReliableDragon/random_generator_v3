
import logging
from typing import Iterable
from random_parser.base_parser import BaseParser

from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.utils import generate_err_msg


class GeneratorParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int):
        super().__init__(filename, lines, line_num)
        self.name = None
        self.choice_block = None

    def parse_generator(self):
        assert self.lines, self.err_msg('Empty file provided')
        self.name = self.use_line()
        logging.info(f'Starting to parse generator "{self.name}".')

        assert self.line() == '', self.err_msg(
            'Generator did not contain a name and choice body separated by a newline')
        self.use_line()

        assert self.lines, self.err_msg('Generator did not contain a choice body')
        self.choice_block = ChoiceBlockParser(self.filename, self.lines, self.line_num)
        self.choice_block.parse()
        self.line_num = self.choice_block.line_num

        return self
