from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.command_expression_parser import CommandExpressionParser
from random_parser.constants import COMMAND_EXPRESSION_MARKER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER, TEXT_EXPRESSION_CONTROL_MARKERS
from random_parser.control_marker import ControlMarker

from random_parser.token_parser import TokenParser


class TextFragmentParser(TokenParser):
    # TODO: Factor out common logic for classes that are parsing lines into different fragments.
    # e.g. ChoiceExpressionParser doing TextFragmentParser, InterpolationTokenParser, and 
    # ImportInterpolationTokenParser, and TextFragmentParser doing RawTextFragments and 
    # CommandExpressionParser.

    pass