from dataclasses import dataclass
import logging
import re
from typing import TYPE_CHECKING, Iterable


from random_parser.base_parser import BaseParser
from random_parser.choice_marker import ChoiceMarkerParser
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, CHOICE_EXPRESSION_END, IMPORT_INTERPOLATION_MARKER, INTERPOLATION_MARKER
from random_parser.context import Context
from random_parser.control_marker import ControlMarker
from random_parser.text_fragment import TextFragmentParser
from random_parser.token_parser import TokenParser

if TYPE_CHECKING:
    from random_parser.interpolation_block import InterpolationBlockParser


class ChoiceExpressionParser(TokenParser):

    def __init__(self, parser: BaseParser, char_num: int):
        super().__init__(base_parser=parser, char_num=char_num)
        self.fragments = []  # Iterable[Union[TextFragmentParser, ChoiceMarkerParser]]
        self.fragment_counts = {
            'interpolation': 0,
            'import': 0,
            'text': 0,
            'marker': 0,
        }

    def evaluate(self, context: Context, interpolation_blocks: Iterable['InterpolationBlockParser']):
        generation = ''
        i = 0
        for fragment in self.fragments:
            logging.debug(generation)
            if isinstance(fragment, TextFragmentParser):
                generation += fragment.evaluate(context)
            elif isinstance(fragment, ChoiceMarkerParser):
                generation += fragment.evaluate(context, interpolation_blocks)
            else:
                raise ValueError(f'Unsupported fragment received: {fragment}')

        return generation

    def _get_control_markers(self):
        return [ControlMarker(c, i) for i, c in enumerate(
            self.expression) if c in CHOICE_EXPRESSION_CONTROL_MARKERS]

    def num_interpolation_fragments(self):
        return self.fragment_counts['interpolation']

    def parse(self):
        logging.debug(f'Parsing choice expression from: {self.line()[self.char_num:]}')
        while not self.is_eol():
            self.fragment_counts['text'] += 1
            text_fragment = TextFragmentParser(self, token_num=self.fragment_counts['text'])
            text_fragment.parse()
            self.sync(text_fragment)
            self.fragments.append(text_fragment)

            if not self.is_eol() and self.char() in CHOICE_EXPRESSION_CONTROL_MARKERS:
                self.fragment_counts['marker'] += 1
                choice_marker = ChoiceMarkerParser(self, self.fragment_counts)
                choice_marker.parse()
                self.sync(choice_marker)
                self.fragments.append(choice_marker)
        self.use_line()  # Consume choice expression line
        return self
