import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, INTERPOLATION_MARKER, WEIGHTED_CHOICE_SEPARATOR
from random_parser.token_parser import TokenParser
from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.text_fragment_parser import TextFragmentParser


class WeightedChoiceParser(TokenParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, expression: str, char_num: int, token_num: int):
        super().__init__(filename, lines, line_num, expression, char_num, token_num)
        self.weight = None  # int
        self.choice_value = None # Union[ChoiceBlockParser, TextFragmentParser]

    def parse_nested_choice_block(self, choice_expression):
        nested_choice_block = ChoiceBlockParser(self.filename, self.lines, self.line_num)
        nested_choice_block.parse_nested(choice_expression)
        self.line_num = nested_choice_block.line_num
        self.choice_value = nested_choice_block
        return nested_choice_block

    def validate(self):
        assert self.weight is not None, self.err_msg('Got null weight when parsing weighted choice')
        assert self.choice_value

    def parse(self):

        choice_line = self.line()
        # Process a single weight/choice line.
        if choice_line.isdecimal():
            self.weight = int(choice_line)
            self.choice_value = TextFragmentParser.empty()
            self.use_line()
            self.validate()
            return self

        weight, choice_value = choice_line.split(WEIGHTED_CHOICE_SEPARATOR, maxsplit=1)

        assert weight.isdecimal(), self.err_msg(f'Got invalid weight {weight}')
        self.weight = int(weight)

        # Check if this is a nested choice block.
        if any(marker in choice_value for marker in CHOICE_EXPRESSION_CONTROL_MARKERS):
            self.parse_nested_choice_block(choice_value)
            self.validate()
            return self

        self.choice_value = TextFragmentParser(self.filename, self.lines, self.line_num, choice_value, 0, 1)
        self.choice_value.parse()
        self.line_num = self.choice_value.line_num

        self.validate()
        return self