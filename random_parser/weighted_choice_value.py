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
        self.choice_value = None  # Union[TextFragmentParser, ChoiceBlockParser]

    def evaluate(self, context: Context):
        return self.choice_value.evaluate(context)

    def parse_nested_choice_block(self):
        nested_choice_block = ChoiceBlockParser(self)
        nested_choice_block.parse_nested(self.char_num)
        self.sync(nested_choice_block)
        self.choice_value = nested_choice_block
        return nested_choice_block

    def parse_text_fragment(self):
        text_fragment = TextFragmentParser(self)
        text_fragment.parse()
        self.sync(text_fragment)
        self.use_line()  # Consume the line, as we've reached the end.
        self.choice_value = text_fragment

    def parse(self):
        starting_char = self.char_num
        is_choice_block = False
        while not self.is_eol():
            if self.use_char() in CHOICE_EXPRESSION_CONTROL_MARKERS:
                is_choice_block = True
        self.char_num = starting_char
        if is_choice_block:
            self.parse_nested_choice_block()
        else:
            self.parse_text_fragment()

        return self