from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, Iterable
from random_parser.context import Context
from random_parser.import_interpolation import ImportInterpolationTokenParser
from random_parser.constants import GENERATOR_PARSER, IMPORT_INTERPOLATION_MARKER, INTERPOLATION_MARKER, RESOURCE_PARSER
from random_parser.interpolation_token import InterpolationTokenParser
from random_parser.token_parser import TokenParser


class ChoiceMarkerParser(TokenParser):

    def __init__(self, parser: TokenParser, fragment_counts: Dict[str: int]):
        super().__init__(parser, token_num=fragment_counts['marker'])
        self.marker = None  # Union[InterpolationTokenParser, ImportInterpolationTokenParser]
        self.fragment_counts = fragment_counts

    def evaluate(self, context: Context, interpolation_blocks: Iterable[InterpolationBlockParser]):
        if isinstance(self.marker, ImportInterpolationTokenParser):
            return self.marker.evaluate(context)
        elif isinstance(self.marker, InterpolationTokenParser):
            # TODO: *Should* token nums be 1-based? This is a footgun.
            fragment_num = self.marker.token_num - 1  # Token nums are 1-based
            return interpolation_blocks[fragment_num].evaluate(context)
        else:
            raise ValueError(f'Unsupported marker received: {self.marker}')

    def parse(self):
        logging.debug(f'Parsing choice marker from: {self.context()}')
        assert self.char() in [INTERPOLATION_MARKER, IMPORT_INTERPOLATION_MARKER], self.err_msg(
            f'Got invalid marker')
        if self.char() == INTERPOLATION_MARKER:
            self.fragment_counts['interpolation'] += 1
            marker = InterpolationTokenParser(self, token_num=self.fragment_counts['interpolation'])
        elif self.char() == IMPORT_INTERPOLATION_MARKER:
            self.fragment_counts['import'] += 1
            marker = ImportInterpolationTokenParser(self, token_num=self.fragment_counts['import'])

        marker.parse()
        self.sync(marker)
        self.marker = marker
        return self

if TYPE_CHECKING:
    from random_parser.interpolation_block import InterpolationBlockParser