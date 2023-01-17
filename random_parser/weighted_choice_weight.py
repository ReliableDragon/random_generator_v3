import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, INTERPOLATION_MARKER, WEIGHTED_CHOICE_END, WEIGHTED_CHOICE_SEPARATOR
from random_parser.context import Context
from random_parser.token_parser import TokenParser
from random_parser.choice_block import ChoiceBlockParser
from random_parser.text_fragment import TextFragmentParser

class WeightedChoiceValueParser(TokenParser):

    def __init__(self, parser: TokenParser):
        super().__init__(parser)
        self.weight = None  # Union[TextFragmentParser, ChoiceBlockParser]
        self.in_command_weight = False

    def parse_weight(self, token):
        if token.isdecimal():
            return int(token)
        elif token.startswith(WEIGHTED_CHOICE_OPEN_DELIMITER):

        raise ValueError(self.err_msg(f'Got invalid weight "{token}"'))

    def is_next_char_valid(self):
        if self.is_eol():
            return False
        if not self.in_command_weight and self.char() == WEIGHTED_CHOICE_SEPARATOR:
            return False
        if self.in_command_weight and self.char() == WEIGHTED_CHOICE_CLOSE_DELIMITER:
            return False
        return True

    def parse(self):
        token = ''
        while self.is_next_char_valid():
            token += self.use_char()
        self.weight = self.parse_weight(token)