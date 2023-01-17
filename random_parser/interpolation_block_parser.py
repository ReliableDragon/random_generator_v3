
import logging
from typing import Dict, Iterable, Union

from random_parser.base_parser import BaseParser
from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, WEIGHTED_CHOICE_SEPARATOR, INTERPOLATION_BLOCK_END, INTERPOLATION_MARKER
from random_parser.weighted_choice_parser import WeightedChoiceParser


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

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, block_num: int = None, choice_expression: str = None):
        super().__init__(filename, lines, line_num)
        self.weighted_choices = []  # Iterable[WeightedChoiceParser]
        self.block_num = block_num  # int
        self.choice_expression = choice_expression  # Optiona[str]

    def __str__(self):
        # TODO: Actually code this.
        return str(self.choice_expression)

    def has_choice_expression(self):
        return self.choice_expression is not None

    def get_while_msg(self):
        if self.has_choice_expression():
            return f'while parsing fragment #{self.block_num} needed for "{self.choice_expression}"'
        else:
            return 'while parsing non-choice-block interpolation_block'

    def parse(self):
        token_num = 1
        while True:
            assert not self.is_finished(), self.err_msg(
                f'Ran out of input {self.get_while_msg()}')
            assert self.line(), self.err_msg(
                f'Got empty line {self.get_while_msg()}')
            logging.debug(f'{self.line_num}: {self.line()}')

            # The dollar sign indicated the end of a subchoice block.
            if self.line() == INTERPOLATION_BLOCK_END:
                logging.debug(f'Found end of interpolation block for interpolation block #{self.block_num} for choice expression "{self.choice_expression}" at line {self.get_line_num()}')
                self.use_line()
                return self

            weighted_choice = WeightedChoiceParser(self.filename, self.lines, self.line_num, self.line(), 0, token_num)
            weighted_choice.parse()
            self.line_num = weighted_choice.line_num
            self.weighted_choices.append(weighted_choice)
            token_num += 1
