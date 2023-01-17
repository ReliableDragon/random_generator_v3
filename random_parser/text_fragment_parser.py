from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.command_expression_parser import CommandExpressionParser
from random_parser.constants import COMMAND_EXPRESSION_MARKER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER, TEXT_EXPRESSION_CONTROL_MARKERS
from random_parser.control_marker import ControlMarker

from random_parser.token_parser import TokenParser


class TextFragmentParser(TokenParser):

    @dataclass
    class RawTextFragment():
        def __init__(self, text, i):
            self.start = i
            self.end = i + len(text)
            self.text = text

    def __init__(
            self, filename: str, lines: Iterable[str],
            line_num: int, expression: str, char_num: int, token_num: int):
        super().__init__(filename, lines, line_num, expression, char_num, token_num)
        self.fragments = []
        self.num_text_fragments = 0
        self.num_command_fragments = 0

        assert self.expression is not None, self.err_msg('Can\'t parse null text fragment!')

    def __str__(self):
        return self.expression

    def _get_control_markers(self):
        return [ControlMarker(c, i) for i, c in enumerate(
            self.expression) if c in TEXT_EXPRESSION_CONTROL_MARKERS]

    def empty():
        return TextFragmentParser('', [], 0, '', 0, 0)

    def parse(self):
        logging.info(
            f'Parsing text fragment {self.expression}')
        control_markers = self._get_control_markers()
        for n, marker in enumerate(control_markers):
            logging.debug(
                f'Parsing marker {marker.marker} (#{n+1} of {len(control_markers)}) for text fragment')
            assert marker.marker in TEXT_EXPRESSION_CONTROL_MARKERS, self.err_msg(
                f'Got invalid marker {marker}')

            self.num_text_fragments += 1
            self.fragments.append(
                self.RawTextFragment(self.expression[self.char_num: marker.index], self.char_num))
            self.char_num = marker.index

            if marker.marker == COMMAND_EXPRESSION_MARKER:
                self.num_command_fragments += 1
                command = CommandExpressionParser(
                    self.filename, self.lines, self.line_num, self.expression, self.char_num, 
                    self.num_command_fragments)
                command.parse()
                self.char_num = command.char_num

                logging.info(f'Finished parsing command: {command}')
                self.fragments.append(command)

        # This assumes that the text goes to the end of the provided line. Could change later.
        if self.char_num != len(self.expression):
            self.num_text_fragments += 1
            self.fragments.append(self.RawTextFragment(self.expression[self.char_num:], self.char_num))

        self.use_line()
        return self
