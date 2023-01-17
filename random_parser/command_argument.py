from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable, Union
from random_parser.constants import COMMAND_ARGUMENT_SEPARATOR, COMMAND_EXPRESSION_CLOSE_DELIMITER, COMMAND_EXPRESSION_MARKER, COMMAND_EXPRESSION_OPEN_DELIMITER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER
from random_parser.context import Context

from random_parser.token_parser import TokenParser


class CommandArgumentParser(TokenParser):

    def __init__(self, parser: TokenParser):
        super().__init__(parser)
        self.argument = None  # Union[str, CommandParser]

    def evaluate(self, context: Context):
        if isinstance(self.argument, str):
            return self.argument
        elif isinstance(self.argument, CommandParser):
            return self.argument.evaluate(context)
        else:
            raise ValueError(f'Got invalid argument: {self.argument}')

    def get_type(self):
        if isinstance(self.argument, str):
            return str
        elif isinstance(self.argument, CommandParser):
            return self.argument.get_type()

    def is_int(self):
        if isinstance(self.argument, str):
            try:
                int(self.argument)
                return True
            except ValueError:
                return False
        elif isinstance(self.argument, CommandParser):
            return self.argument.get_type() == int

    def is_str(self):
        if isinstance(self.argument, str):
            return True
        elif isinstance(self.argument, CommandParser):
            return self.argument.get_type() == str

    def parse_nested_command(self, command):
        self.argument = CommandParser(self)
        self.argument.parse_nested(command)
        self.sync(self.argument)

    def is_next_char_valid(self):
        return self.char() not in [
            COMMAND_ARGUMENT_SEPARATOR, 
            COMMAND_EXPRESSION_OPEN_DELIMITER, 
            COMMAND_EXPRESSION_CLOSE_DELIMITER]

    def parse(self):
        argument = ''
        while self.is_next_char_valid():
            c = self.use_char()
            if c != ' ':  # Skip whitespace
                argument += c

            assert not self.is_eol(), self.err_msg(
                f'Reached EOL while parsing arguments {self.arguments} for command'
                    f'{self.command}! (Did you forget a closing parenthesis?)')

        if self.char() in [COMMAND_ARGUMENT_SEPARATOR, COMMAND_EXPRESSION_CLOSE_DELIMITER]:
            self.argument = argument
        elif self.char() == COMMAND_EXPRESSION_OPEN_DELIMITER:
            self.parse_nested_command(argument)

        logging.debug(f'Parsed argument {self.argument}')
        return self

        
from random_parser.command import CommandParser