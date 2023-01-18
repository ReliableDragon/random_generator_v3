
import logging
from typing import Iterable

# Abstract


class BaseParser():
    """Base class for parsers.

    Attributes:
    filename: String filename indicating the name (not filepath) of the file being processed.
    lines: List containing all the lines to process.
    line_num: 0-indexed line number that is currently being processed."""

    def __init__(
            self, parser: 'BaseParser' = None, filename: str = None, lines: Iterable[str] = None,
            line_num: int = None):
        if parser:
            self.filename = parser.filename
            self.lines = parser.lines
            self.line_num = parser.line_num
        else:
            self.filename = filename
            self.lines = lines
            self.line_num = line_num
        assert self.filename, 'Filename was not initialized!'
        assert self.lines, f'Lines was not initialized for file {self.filename}!'
        assert self.line_num is not None, f'Line num was not initialized for file {self.filename}!'

    def line(self):
        try:
            return self.lines[self.line_num].lstrip()
        except IndexError as e:
            logging.error(f'{self._msg_intro()} Attempted to consume line past end of file!')
            raise e

    def use_line(self):
        line = self.line()
        self.line_num += 1
        return line

    def get_line_num(self):
        return self.line_num + 1  # 0-indexing vs 1-indexing my beloathed

    def is_finished(self):
        return self.line_num == len(self.lines)

    def context(self):
        return self.line()[:25]

    def sync(self, other):
        self.line_num = other.line_num

    def err_msg(self, msg):
        if self.is_finished():
            line_contents = '<EOF>'
        else:
            line_contents = self.line()
        return f'{self._msg_intro()} {msg}: "{line_contents}"'

    def _msg_intro(self):
        return f'{self.__class__.__name__}, file {self.filename}, line {self.line_num+1}>'
