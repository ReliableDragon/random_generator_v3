from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable, Union
from random_parser.commands.command import CommandParser
from random_parser.constants import COMMAND_ARGUMENT_SEPARATOR, COMMAND_EXPRESSION_CLOSE_DELIMITER, COMMAND_EXPRESSION_MARKER, COMMAND_EXPRESSION_OPEN_DELIMITER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER
from random_parser.context import Context

from random_parser.token_parser import TokenParser


class CommandExpressionParser(TokenParser):

    def __init__(self, parser: TokenParser, is_integer: bool = False):
        super().__init__(parser)
        self.is_integer = is_integer
        self.command = None  # CommandParser

    def evaluate(self, context: Context):
        logging.info(f'Evaluating command expression {self})')
        return str(self.command.evaluate(context))  # Convert to string context

    # TODO: Add repeated command capabilities by switching to an array of command
    # fragments, so that things like arithemetic can be done.
    def parse(self):
        assert self.char() == COMMAND_EXPRESSION_MARKER, self.err_msg('Got invalid token to start command expression')
        self.use_char()  # Consume opening command expression "#"
        assert self.char() == COMMAND_EXPRESSION_OPEN_DELIMITER, self.err_msg(f'Command expression marker was not followed by "{COMMAND_EXPRESSION_OPEN_DELIMITER}"')
        self.use_char()  # Consume leading command expression "("

        self.command = CommandParser(self, self.is_integer)
        self.command.parse()
        self.sync(self.command)

        assert self.char() == COMMAND_EXPRESSION_CLOSE_DELIMITER, self.err_msg(f'Command expression was not followed by "{COMMAND_EXPRESSION_CLOSE_DELIMITER}" (Did you forget a closing parenthesis?)')
        self.use_char()  # Consume trailing command expression ")"

        return self