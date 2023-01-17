from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable

from random_parser.token_parser import TokenParser


class TextFragmentParser(TokenParser):
    # TODO: Factor out common logic for classes that are parsing lines into different fragments.
    # e.g. ChoiceExpressionParser doing TextFragmentParser, InterpolationTokenParser, and 
    # ImportInterpolationTokenParser, and TextFragmentParser doing RawTextFragments and 
    # CommandExpressionParser.

    pass