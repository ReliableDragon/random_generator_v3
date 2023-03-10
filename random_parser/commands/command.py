from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable, Union
from random_parser.commands.commands import Commands
from random_parser.constants import COMMAND_ARGUMENT_SEPARATOR, COMMAND_EXPRESSION_CLOSE_DELIMITER, COMMAND_EXPRESSION_MARKER, COMMAND_EXPRESSION_OPEN_DELIMITER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER
from random_parser.context import Context

from random_parser.token_parser import TokenParser


class CommandParser(TokenParser):

    def __init__(self, parser: TokenParser, is_integer: bool = False):
        super().__init__(parser)
        self.is_integer = is_integer
        self.command_name = None  # str
        self.arguments = []  # Iterable[Union[ArgumentFragment, Command]]
        self.command = None  # Commands.Command

    def get_type(self):
        return self.command.type

    def evaluate(self, context: Context):
        evaluated_arguments = []
        for argument in self.arguments:
            evaluated_arguments.append(argument.evaluate(context))
        return self.command.evaluate(evaluated_arguments)

    def validate_types(self):
        assert len(self.arguments) == len(self.command.arg_types), self.err_msg(
            f'Expected {len(self.command.arg_types)} arguments for command {self.command.name}, '
            f'but got {len(self.arguments)}')

        for i, arg_type in enumerate(self.command.arg_types):
            if arg_type == int:
                assert self.arguments[i].is_int(), self.err_msg(
                    f'Command {self.command_name} expected arguments of types '
                    f'{self.command.arg_types}, but got {self.arguments}, which are not compatible.')
            elif arg_type == str:
                assert self.arguments[i].is_str(), self.err_msg(
                    f'Command {self.command_name} expected arguments of types '
                    f'{self.command.arg_types}, but got {self.arguments}, which are not compatible.')

    def parse_argument(self):
        argument_parser = CommandArgumentParser(self)
        argument_parser.parse()
        self.sync(argument_parser)
        self.arguments.append(argument_parser)

    def parse_arguments(self):
        assert not self.is_eol(), self.err_msg(
            f'Expected arguments for command {self.command}, but got EOL instead')
        if self.char() == COMMAND_EXPRESSION_CLOSE_DELIMITER:
            # No arguments
            return
        while True:
            self.parse_argument()
    
            assert self.char() in [COMMAND_ARGUMENT_SEPARATOR, 
            COMMAND_EXPRESSION_CLOSE_DELIMITER], self.err_msg(
                f'Got invalid character after parsing argument "{self.char()}"')

            assert not self.is_eol(), self.err_msg(
                f'Reached EOL while parsing arguments {self.arguments} for command '
                f'{self.command}! (Did you forget a closing parenthesis?)')

            if self.char() == COMMAND_EXPRESSION_CLOSE_DELIMITER:
                break
            elif self.char() == COMMAND_ARGUMENT_SEPARATOR:
                self.use_char()

        self.validate_types()

    def _set_command(self, command):
        assert command in Commands.COMMANDS, self.err_msg(f'Got unsupported command name: "{command}"')
        self.command = Commands.COMMANDS[command]
        if self.is_integer:
            assert self.command.type == int, self.err_msg(f'Got command of type {self.command.type} in integer command context')
        logging.debug(f'Set command {command}')

    def parse_command_name(self):
        command_name = ''
        while self.char() != COMMAND_EXPRESSION_OPEN_DELIMITER:
            command_name += self.use_char()
        self._set_command(command_name)

    # Special case for entering from argument where name is already parsed
    def parse_nested(self, command_name):
        self._set_command(command_name)
        return self._parse()

    def parse(self):
        self.parse_command_name()
        return self._parse()

    def _parse(self):
        self.use_char()  # Consume leading "("
        self.parse_arguments()
        self.use_char()  # Consume trailing ")"
        return self

from random_parser.commands.command_argument import CommandArgumentParser