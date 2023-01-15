
import logging
from typing import Dict, Iterable

from random_parser.base_parser import BaseParser


class SubchoiceParser(BaseParser):
    """Parser for subchoices, the lists of elements and weights from which choices are made.

    Attributes:
    choices: A list of choices. Must be kept in order with weights.
    weights: A list of weights. Must be kept in order with choices.
    choice_header: The header line for the choice body. Debugging purposes only.
    fragment_num: Which fragment is currently being parsed. Debugging purposes only."""

    choices: Iterable[str]
    weights: Iterable[int]
    choice_header: str
    fragment_num: int

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, fragment_num: int, choice_header: str):
        super().__init__(filename, lines, line_num)
        self.choice_header = choice_header
        self.choices = []
        self.weights = []
        self.fragment_num = fragment_num

    def __str__(self):
        return str(self.choices)

    def parse(self):
        while True:
            assert not self.is_finished(), self.err_msg(
                f'Ran out of input while parsing fragment #{self.fragment_num} needed for "{self.choice_header}"')
            assert self.line(), self.err_msg(
                f'Got empty line while parsing fragment #{self.fragment_num} needed for "{self.choice_header}"')
            logging.debug(f'{self.line_num}: {self.line()}')

            # The dollar sign indicated the end of a subchoice block.
            if self.line() == '$':
                self.use_line()
                return self

            # Process a single weight/choice line.
            choice_line = self.use_line()
            weight, choice = choice_line.split(' ', maxsplit=1)

            assert weight.isdecimal(), self.err_msg(f'Got invalid weight {weight}')
            weight = int(weight)

            self.choices.append(choice)
            self.weights.append(weight)
