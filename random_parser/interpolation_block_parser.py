
import logging
from typing import Dict, Iterable, Union

from random_parser.base_parser import BaseParser
from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, WEIGHTED_CHOICE_SEPARATOR, INTERPOLATION_BLOCK_END, INTERPOLATION_MARKER


class InterpolationBlockParser(BaseParser):
    """Parser for interpolation blocks, the lists of elements and weights from which choices are made.

    This class can be called either as part of a choice block, or as the top level of a resource
    file, so there's some special logic to provide extra debugging information in the choice
    block case.

    Attributes:
    choices: A list of choices. Must be kept in order with weights.
    weights: A list of weights. Must be kept in order with choices.
    choice_header: The header line for the choice body. Debugging purposes only.
    fragment_num: Which fragment is currently being parsed. Debugging purposes only."""

    choice_expression: str
    block_num: int  # 1-indexed
    choices: Iterable[Union[str, ChoiceBlockParser]]
    weights: Iterable[int]

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, block_num: int = None, choice_expression: str = None):
        super().__init__(filename, lines, line_num)
        self.choice_expression = choice_expression  # str
        self.block_num = block_num  # int
        self.choices = []  # Iterable[Union[str, ChoiceBlockParser]]
        self.weights = []  # Iterable[int]

    def print(self, indent = 0, top_level = False):
        rep = ''
        if top_level:
            rep += super().print(indent)
        rep += ' ' * indent + 'choice_expression: ' + self.choice_expression + '\n'
        rep += ' ' * indent + 'block_num: ' + str(self.block_num) + '\n'
        rep += self.print_choices(indent)
        rep += ' ' * indent + 'weights: ' + str(self.weights) + '\n'
        return rep

    def print_choices(self, indent=0, top_level=False):
        rep = ''
        rep += ' ' * indent + 'choices:' + '\n'
        rep += '\n'.join([' ' * indent + (l if isinstance(l, str) else l.print(indent+4)) for l in self.choices]) + '\n'
        return rep

    def __str__(self):
        return str(self.choices)


    def has_choice_expression(self):
        return self.choice_expression is not None

    def parse_nested_choice_block(self, choice_expression):
        nested_choice_block = ChoiceBlockParser(self.filename, self.lines, self.line_num)
        nested_choice_block.parse_nested(choice_expression)
        self.line_num = nested_choice_block.line_num
        return nested_choice_block

    def get_while_msg(self):
        if self.has_choice_expression():
            return f'while parsing fragment #{self.block_num} needed for "{self.choice_expression}"'
        else:
            return 'while parsing non-choice-block interpolation_block'

    def parse(self):
        while True:
            assert not self.is_finished(), self.err_msg(
                f'Ran out of input {self.get_while_msg()}')
            assert self.line(), self.err_msg(
                f'Got empty line {self.get_while_msg()}')
            logging.debug(f'{self.line_num}: {self.line()}')

            # The dollar sign indicated the end of a subchoice block.
            if self.line() == INTERPOLATION_BLOCK_END:
                logging.debug(f'Found end of interpolation block for choice expression {self.choice_expression} at line {self.get_line_num()}')
                self.use_line()
                return self

            choice_line = self.line()
            # Process a single weight/choice line.
            if choice_line.isdecimal():
                weight = choice_line
                choice = ''
            else:
                weight, choice = choice_line.split(WEIGHTED_CHOICE_SEPARATOR, maxsplit=1)

            # Check if this is a nested choice block.
            if any(marker in choice for marker in CHOICE_EXPRESSION_CONTROL_MARKERS):
                choice = self.parse_nested_choice_block(choice)
            else:
                self.use_line()

            assert weight.isdecimal(), self.err_msg(f'Got invalid weight {weight}')
            weight = int(weight)

            self.choices.append(choice)
            self.weights.append(weight)
