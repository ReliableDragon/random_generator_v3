import logging
import re
from typing import Iterable


from random_parser.base_parser import BaseParser
from random_parser.choice_expression_parser import ChoiceExpressionParser
from random_parser.choice_marker_parser import ChoiceMarkerParser
from random_parser.constants import GENERATOR_PARSER, RESOURCE_PARSER
from random_parser.context import Context
from random_parser.text_fragment_parser import TextFragmentParser
from random_parser.import_interpolation_token_parser import ImportInterpolationTokenParser
from random_parser.interpolation_token_parser import InterpolationTokenParser


class ChoiceBlockParser(BaseParser):

    def __init__(self, parser: BaseParser):
        super().__init__(parser)
        self.choice_expression_parser = None  # ChoiceExpressionParser
        self.interpolation_blocks = []  # Iterable[InterpolationBlockParser]

    def evaluate(self, context: Context):
        logging.debug(f'Evaluating...')
        return self.choice_expression_parser.evaluate(context, self.interpolation_blocks)

    def parse(self):
        assert self.line(), self.err_msg('Empty choice body')
        self._parse(0)
        return self

    # Special entry point for coming from weighted choice lines
    def parse_nested(self, char_num: int):
        # Trim off the beginning with the weight
        self._parse(char_num)
        return self

    def _parse(self, char_num: int):
        logging.debug(f'Processing choice block for "{self.line()[char_num:]}"')
        self.choice_expression_parser = ChoiceExpressionParser(self, char_num=char_num)
        self.choice_expression_parser.parse()
        self.sync(self.choice_expression_parser)

        num_itpl_fragments = self.choice_expression_parser.num_interpolation_fragments()
        for block_num in range(1, num_itpl_fragments+1):  # Add 1 for 1-indexing
            logging.info(f'Parsing interpolation block index #{block_num} of {num_itpl_fragments}')
            interpolation_block = interpolation_block_parser.InterpolationBlockParser(
                self, block_num, self.line()[char_num:])
            interpolation_block.parse()
            self.interpolation_blocks.append(interpolation_block)
            self.sync(interpolation_block)
            logging.info(f'Finished parsing fragment: {interpolation_block}')


    def length(self):
        return len(self.interpolation_blocks)


# Delay import to prevent circular dependencies.
import random_parser.interpolation_block_parser as interpolation_block_parser