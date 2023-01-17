import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, INTERPOLATION_MARKER, WEIGHTED_CHOICE_END, WEIGHTED_CHOICE_SEPARATOR
from random_parser.context import Context
from random_parser.token_parser import TokenParser
from random_parser.base_parser import BaseParser
from random_parser.weighted_choice_value import WeightedChoiceValueParser


class WeightedChoiceParser(TokenParser):

    def __init__(self, parser: BaseParser, char_num: int, token_num: int):
        super().__init__(base_parser=parser, char_num=char_num, token_num=token_num)
        self.weight = None  # int
        self.choice_value = None # WeightedChoiceValueParser

    def evaluate(self, context: Context):
        raise NotImplemented('Attemped to evaluate data-only parser!')

    def validate(self):
        assert self.weight is not None, self.err_msg('Got null weight when parsing weighted choice')
        assert self.choice_value

    def parse(self):
        # Technically this should be done by character since this is a token parser,
        # but right now this one is simple enough that we'll cheat and use the line.
        token = ''
        while not self.is_eol() and self.char() != WEIGHTED_CHOICE_SEPARATOR:
            token += self.use_char()
        assert token.isdecimal(), self.err_msg(f'Got invalid weight "{token}"')
        self.weight = int(token)
        if not self.is_eol():
            self.use_char()  # Consume trailing space.
        
        # We still parse this token, even if the weight ended with EOL, as it will provide a
        # 0-length TextFragment and consume the line, which is technically what we want.
        token = ''
        self.choice_value = WeightedChoiceValueParser(self)
        self.choice_value.parse()
        self.sync(self.choice_value)

        self.validate()
        return self