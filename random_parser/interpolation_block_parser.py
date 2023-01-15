
import logging
from typing import Dict, Iterable, Union

from random_parser.base_parser import BaseParser
from random_parser.choice_block_parser import ChoiceBlockParser


class InterpolationBlockParser(BaseParser):
    """Parser for interpolation blocks, the lists of elements and weights from which choices are made.

    Attributes:
    choices: A list of choices. Must be kept in order with weights.
    weights: A list of weights. Must be kept in order with choices.
    choice_header: The header line for the choice body. Debugging purposes only.
    fragment_num: Which fragment is currently being parsed. Debugging purposes only."""

    choices: Iterable[Union[str, ChoiceBlockParser]]
    weights: Iterable[int]
    choice_expression: str
    fragment_num: int

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, fragment_num: int, choice_expression: str):
        super().__init__(filename, lines, line_num)
        self.choice_expression = choice_expression
        self.choices = []
        self.weights = []
        self.fragment_num = fragment_num

    def __str__(self):
        return str(self.choices)

    def parse_nested_choice_block(self, choice_expression):
        nested_choice_block = ChoiceBlockParser(self.filename, self.lines, self.line_num)
        nested_choice_block.parse_nested(choice_expression)
        self.line_num = nested_choice_block.line_num
        return nested_choice_block

    def parse(self):
        while True:
            assert not self.is_finished(), self.err_msg(
                f'Ran out of input while parsing fragment #{self.fragment_num} needed for "{self.choice_expression}"')
            assert self.line(), self.err_msg(
                f'Got empty line while parsing fragment #{self.fragment_num} needed for "{self.choice_expression}" (Did you forget to close a fragment with "$"?)')
            logging.debug(f'{self.line_num}: {self.line()}')

            # The dollar sign indicated the end of a subchoice block.
            if self.line() == '$':
                self.use_line()
                return self

            # Process a single weight/choice line.
            choice_line = self.use_line()
            if choice_line.isdecimal():
                weight = choice_line
                choice = ''
            else:
                weight, choice = choice_line.split(' ', maxsplit=1)

            if '$' in choice:
                choice = self.parse_nested_choice_block(choice)

            assert weight.isdecimal(), self.err_msg(f'Got invalid weight {weight}')
            weight = int(weight)

            self.choices.append(choice)
            self.weights.append(weight)
