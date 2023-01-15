import logging
import re
from typing import Iterable


from random_parser.base_parser import BaseParser
from random_parser.choice_expression_parser import ChoiceExpressionParser


class ChoiceBlockParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int):
        super().__init__(filename, lines, line_num)
        self.choice_expression_parser = None  # ChoiceExpressionParser
        self.interpolation_blocks = []  # Iterable[InterpolationBlockParser]

    def print(self, indent = 0, top_level = False):
        rep = ''
        if top_level:
            rep += super().print(indent)
        rep += ' ' * indent + 'expression_parser: ' + self.choice_expression_parser.print(indent + 4) + '\n'
        rep += ' ' * indent + 'interpolation_blocks:' + '\n' + '\n'.join([' ' * indent + l.print(indent + 4) for l in self.interpolation_blocks]) + '\n'
        return rep

    def parse(self):
        assert self.line(), self.err_msg('Empty choice body')
        choice_expression = self.line()  # Choice expressions end with \n currently, but this
                                             # could need to be reworked in the future.
        self._parse(choice_expression)

        return self

    def parse_nested(self, choice_expression):
        self._parse(choice_expression)

        return self

    def _parse(self, choice_expression: str):
        logging.debug(f'Processing choice expression "{choice_expression}"')
        self.choice_expression_parser = ChoiceExpressionParser(self.filename, self.lines, self.line_num, choice_expression)
        self.choice_expression_parser.parse()
        self.line_num = self.choice_expression_parser.line_num

        num_itpl_fragments = self.choice_expression_parser.num_interpolation_fragments
        for block_num in range(1, num_itpl_fragments+1):  # Add 1 for 1-indexing
            logging.info(f'Parsing interpolation at index #{block_num} of {num_itpl_fragments}')
            interpolation_block = interpolation_block_parser.InterpolationBlockParser(
                self.filename, self.lines, self.line_num, block_num, choice_expression)
            interpolation_block.parse()
            self.interpolation_blocks.append(interpolation_block)
            self.line_num = interpolation_block.line_num
            logging.info(f'Finished parsing fragment: {interpolation_block}')


    def length(self):
        return len(self.interpolation_blocks)


# Delay import to prevent circular dependencies.
import random_parser.interpolation_block_parser as interpolation_block_parser