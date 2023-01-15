
import logging
from typing import Iterable

from random_parser.utils import generate_err_msg


class BaseParser():
    """Base class for parsers.
    
    Attributes:
    filename: String filename indicating the name (not filepath) of the file being processed.
    lines: List containing all the lines to process.
    line_num: 0-indexed line number that is currently being processed."""

    def __init__(self, filename: str, lines: Iterable[str], line_num: int):
        self.filename = filename
        self.lines = lines
        self.line_num = line_num

    def print(self, indent = 0):
        rep = ''
        rep += ' ' * indent + 'filename: ' + self.filename + '\n'
        rep += ' ' * indent + 'line_num: ' + str(self.line_num) + '\n'
        rep += ' ' * indent + 'lines:' + '\n' + '\n'.join([' ' * indent + str(l) for l in self.lines]) + '\n'
        return rep

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

    def err_msg(self, msg):
        if self.is_finished():
            line_contents = '<EOF>'
        else:
            line_contents = self.line()
        return f'{self._msg_intro()} {msg}: "{line_contents}"'

    def _msg_intro(self):
        return f'{self.__class__.__name__}, file {self.filename}, line {self.line_num+1}>'
