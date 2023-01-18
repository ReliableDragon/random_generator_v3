from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.commands.command_expression import CommandExpressionParser
from random_parser.constants import CHOICE_EXPRESSION_CONTROL_MARKERS, CHOICE_EXPRESSION_END, COMMAND_EXPRESSION_MARKER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER, TEXT_EXPRESSION_CONTROL_MARKERS
from random_parser.context import Context

from random_parser.token_parser import TokenParser


class TextFragmentParser(TokenParser):

    @dataclass
    class RawTextFragment():
        def __init__(self, text, i):
            self.start = i
            self.end = i + len(text)
            self.text = text

    def __init__(
            self, parser: TokenParser, token_num: int = 1):
        super().__init__(token_parser=parser, token_num=token_num)
        self.fragments = []
        self.num_text_fragments = 0
        self.num_command_fragments = 0

    def evaluate(self, context: Context):
        generation = ''
        for fragment in self.fragments:
            if isinstance(fragment, self.RawTextFragment):
                generation += fragment.text
            elif isinstance(fragment, CommandExpressionParser):
                generation += fragment.evaluate(context)
            else:
                raise ValueError(f'Got invalid text fragment: {fragment}')
        return generation

    def is_next_char_valid(self):
        if self.is_eol():
            return False
        if self.char() in CHOICE_EXPRESSION_CONTROL_MARKERS:
            return False
        return True

    def parse(self):
        fragment = ''
        start = self.char_num
        while self.is_next_char_valid():
            if self.char() == COMMAND_EXPRESSION_MARKER:
                self.num_text_fragments += 1
                self.fragments.append(self.RawTextFragment(fragment, start))

                self.num_command_fragments += 1
                command = CommandExpressionParser(self)
                command.parse()
                self.sync(command)
                self.fragments.append(command)
                fragment = ''
                start = self.char_num
                logging.info(f'Finished parsing command: {command}')
            else:
                fragment += self.use_char()

        self.num_text_fragments += 1
        self.fragments.append(self.RawTextFragment(fragment, start))
        return self
