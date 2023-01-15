import logging
import re
from typing import Iterable


from random_parser.base_parser import BaseParser
from random_parser.constants import IMPORT_INTERPOLATION_MARKER, INTERPOLATION_MARKER
from random_parser.import_interpolation_symbol_parser import ImportInterpolationSymbolParser


class ChoiceBlockParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int):
        super().__init__(filename, lines, line_num)
        self.text_fragments = []
        self.subchoices = []

    def parse(self):
        assert self.line(), self.err_msg('Empty choice body')
        choice_expression = self.use_line()
        self._parse(choice_expression)

        return self

    def parse_nested(self, choice_expression):
        self._parse(choice_expression)

        return self

    def _parse(self, choice_expression: str):
        logging.debug(f'Processing choice expression "{choice_expression}"')
        self.text_fragments = re.split(
            rf'[{INTERPOLATION_MARKER}{IMPORT_INTERPOLATION_MARKER}]', choice_expression)
        
        num_fragments = len(self.text_fragments) - 1  # Subtract one to avoid a fencepost error.
        markers = [INTERPOLATION_MARKER, IMPORT_INTERPOLATION_MARKER]
        marker_indexes = [i for i, c in enumerate(choice_expression) if c in markers]

        fragment_num = 1
        for i in marker_indexes:
            c = choice_expression[i]
            logging.info(f'Parsing interpolation marker {c} for fragment #{fragment_num} of {num_fragments}')
            if c == INTERPOLATION_MARKER:
                subchoice = interpolation_block_parser.InterpolationBlockParser(
                    self.filename, self.lines, self.line_num, fragment_num, choice_expression)
                subchoice.parse()
                self.subchoices.append(subchoice)
                self.line_num = subchoice.line_num
            elif c == IMPORT_INTERPOLATION_MARKER:
                subchoice = ImportInterpolationSymbolParser(
                    self.filename, self.lines, self.line_num, choice_expression, i)
                subchoice.parse()
                self.subchoices.append(subchoice)
                self.line_num = subchoice.line_num
            fragment_num += 1
            logging.info(f'Finished parsing fragment: {subchoice}')


    def length(self):
        return len(self.subchoices)


# Delay import to prevent circular dependencies.
import random_parser.interpolation_block_parser as interpolation_block_parser