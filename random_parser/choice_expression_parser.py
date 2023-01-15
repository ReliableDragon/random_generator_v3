from dataclasses import dataclass
import logging
import re
from typing import Iterable


from random_parser.base_parser import BaseParser
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, IMPORT_INTERPOLATION_MARKER, INTERPOLATION_MARKER
from random_parser.import_interpolation_token_parser import ImportInterpolationTokenParser
from random_parser.interpolation_token_parser import InterpolationTokenParser


class ChoiceExpressionParser(BaseParser):

    @dataclass
    class ControlMarker():
        marker: str
        index: int

        def __str__(self):
            return f'({self.marker}, {self.index})'

    @dataclass
    class TextFragment():
        start: int  # Inclusive
        stop: int  # Exclusive
        text: str

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, choice_expression: str):
        super().__init__(filename, lines, line_num)
        self.choice_expression = choice_expression
        self.fragments = []
        self.num_interpolation_fragments = 0
        self.num_import_itpl_fragments = 0

    def print(self, indent = 0, top_level = False):
        rep = ''
        if top_level:
            rep += super().print(indent)
        rep += ' ' * indent + 'choice_expression: ' + self.choice_expression + '\n'
        rep += ' ' * indent + 'fragments: ' + str(self.fragments) + '\n'
        rep += ' ' * indent + 'num_interpolation_fragments: ' + str(self.num_interpolation_fragments) + '\n'
        rep += ' ' * indent + 'num_import_itpl_fragments: ' + str(self.num_import_itpl_fragments) + '\n'
        return rep

    def get_control_markers(self):
        return [self.ControlMarker(c, i) for i, c in enumerate(
            self.choice_expression) if c in CHOICE_EXPRESSION_CONTROL_MARKERS]

    def parse(self):
        control_markers = self.get_control_markers()
        i = 0
        for n, marker in enumerate(control_markers):
            logging.info(f'Parsing interpolation marker {marker.marker} for fragment #{n+1} of {len(control_markers)}')
            assert marker.marker in CHOICE_EXPRESSION_CONTROL_MARKERS, self.err_msg(f'Got invalid marker {marker}')
            self.fragments.append(self.TextFragment(i, marker.index, self.choice_expression[i:marker.index]))
            i = marker.index

            if marker.marker == INTERPOLATION_MARKER:
                clazz = InterpolationTokenParser
                # Set fragment_num first, as fragment_num is 0-indexed, while the num_*_fragments
                # fields are 1-based counting. This order saves having to subtract one.
                fragment_num = self.num_interpolation_fragments
                self.num_interpolation_fragments += 1
            elif marker.marker == IMPORT_INTERPOLATION_MARKER:
                clazz = ImportInterpolationTokenParser
                fragment_num = self.num_import_itpl_fragments
                self.num_import_itpl_fragments += 1

            symbol_parser = clazz(
                self.filename, self.lines, self.line_num, self.choice_expression, i, fragment_num)
            symbol_parser.parse()
            i = symbol_parser.char_num

            logging.info(f'Finished parsing fragment: {symbol_parser}')
            self.fragments.append(symbol_parser)

        if i != len(self.choice_expression):
            self.fragments.append(self.TextFragment(i, len(self.choice_expression), self.choice_expression[i:]))

        self.use_line()
        return self