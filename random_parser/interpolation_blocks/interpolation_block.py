
import logging
import random
from typing import Dict, Iterable, Union

from random_parser.base_parser import BaseParser
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, WEIGHTED_CHOICE_SEPARATOR, INTERPOLATION_BLOCK_END, INTERPOLATION_MARKER
from random_parser.context import Context
from random_parser.weighted_choices.weighted_choice import WeightedChoiceParser
from random_parser.weighted_choices.weighted_choice_value import WeightedChoiceValueParser


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
            self, parser: BaseParser, block_num: int = None, parent_choice_expression: str = None):
        super().__init__(parser)
        self.weighted_choices = []  # Iterable[WeightedChoiceParser]
        self.block_num = block_num  # int
        self.parent_choice_expression = parent_choice_expression  # Optional[str]

    def __str__(self):
        # TODO: Actually code this.
        return str(self.parent_choice_expression)

    def randomly_generate_weighted_choice(self, context) -> WeightedChoiceValueParser:
        total_weight= sum([wc.get_weight(context) for wc in self.weighted_choices])
        threshold= random.randint(1, total_weight)
        i= -1  # Start at -1 to ensure loop condition evaluates properly at i=0.
        weight_sum = 0
        while weight_sum < threshold:
            i += 1
            weight_sum += self.weighted_choices[i].get_weight(context)
        choice = self.weighted_choices[i].choice_value
        return choice

    def evaluate(self, context: Context):
        logging.debug(f'Evaluating interpolation block {self}')
        return self.randomly_generate_weighted_choice(context).evaluate(context)

    def has_choice_expression(self):
        return self.parent_choice_expression is not None

    def get_while_msg(self):
        if self.has_choice_expression():
            return f'while parsing fragment #{self.block_num} needed for "{self.parent_choice_expression}"'
        else:
            return 'while parsing non-choice-block interpolation_block'

    def parse(self):
        token_num = 1
        while True:
            logging.debug(f'Line #{self.get_line_num()}: {self.line()}')
            assert not self.is_finished(), self.err_msg(
                f'Ran out of input {self.get_while_msg()}')
            assert self.line(), self.err_msg(
                f'Got empty line {self.get_while_msg()}')

            # The dollar sign indicated the end of a subchoice block.
            if self.line() == INTERPOLATION_BLOCK_END:
                logging.debug(f'Found end of interpolation block for interpolation block #{self.block_num} for choice expression "{self.parent_choice_expression}" at line {self.get_line_num()}')
                self.use_line()
                return self

            weighted_choice = WeightedChoiceParser(self, 0, token_num)
            weighted_choice.parse()
            self.sync(weighted_choice)
            self.weighted_choices.append(weighted_choice)
            token_num += 1