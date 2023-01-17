from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.commands import Commands
from random_parser.constants import COMMAND_ARGUMENT_SEPARATOR, COMMAND_EXPRESSION_CLOSE_DELIMITER, COMMAND_EXPRESSION_MARKER, COMMAND_EXPRESSION_OPEN_DELIMITER, IMPORT_INTERPOLATION_MARKER, IMPORT_ITPL_CLOSE_DELIMITER, IMPORT_ITPL_END, IMPORT_ITPL_OPEN_DELIMITER

from random_parser.token_parser import TokenParser


class CommandExpressionParser(TokenParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int, expression: str, char_num: int, token_num: int):
        super().__init__(filename, lines, line_num, expression, char_num, token_num)
        self.command = None  # Command
        self.arguments = []  # Iterable[Union[ArgumentFragment, Command]]

    def _set_command(self, command):
        assert command in Commands.COMMANDS, self.err_msg(f'Got unsupported command: "{command}"')
        self.command = Commands.COMMANDS[command]

    def parse_nested_command(self, command_name):
        nested_command_expression_parser = CommandExpressionParser(self.filename, self.lines,
        self.line_num, self.expression, self.char_num, self.token_num)
        nested_command_expression_parser._set_command(command_name)
        nested_command_expression_parser.parse_arguments()
        return nested_command_expression_parser

    def parse_command(self):
        command_name = ''
        while self.char() != COMMAND_EXPRESSION_OPEN_DELIMITER:
            command_name += self.use_char()
        self._set_command(command_name)
        self.use_char()
        return self

    def parse_arguments(self):
        argument = ''
        assert not self.is_eol(), self.err_msg(f'Expected arguments for command {self.command}, but got EOL instead')
        while self.char() != COMMAND_EXPRESSION_CLOSE_DELIMITER:
            if self.char() == ' ':
                self.use_char()
            elif self.char() == COMMAND_EXPRESSION_OPEN_DELIMITER:
                self.use_char()  # Consume "(" before recursing, or it'll hit this case immediately
                nested_command = self.parse_nested_command(argument)
                self.char_num = nested_command.char_num
                self.arguments.append(nested_command)
                argument = ''
            elif self.char() == COMMAND_ARGUMENT_SEPARATOR:
                self.arguments.append(Commands.ArgumentFragment(argument))
                self.use_char()
                argument = ''
            else:
                argument += self.use_char()
            assert not self.is_eol(), self.err_msg(f'Reached EOL while parsing arguments {self.arguments} for  command {self.command}! (Did you forget a closing parenthesis?)')
        if argument:
            self.arguments.append(Commands.ArgumentFragment(argument))
        self.use_char()  # Consume trailing ")"

        assert len(self.arguments) == self.command.num_args, f'Expected {self.command.num_args} arguments for command {self.command.name}, but got {len(self.arguments)}'
        return self

    # TODO: Add repeated command capabilities by switching to an array of command
    # fragments, so that things like arithemetic can be done.
    def parse(self):
        assert self.char() == COMMAND_EXPRESSION_MARKER, self.err_msg('Got invalid token to start command expression')
        self.use_char()  # Consume opening command expression "#"
        assert self.char() == COMMAND_EXPRESSION_OPEN_DELIMITER, self.err_msg(f'Command expression marker was not followed by "{COMMAND_EXPRESSION_OPEN_DELIMITER}"')
        self.use_char()  # Consume leading command expression "(" 

        self.parse_command()
        self.parse_arguments()

        assert self.char() == COMMAND_EXPRESSION_CLOSE_DELIMITER, self.err_msg(f'Command expression arguments were not followed by "{COMMAND_EXPRESSION_CLOSE_DELIMITER}" (Did you forget a closing parenthesis?)')
        self.use_char()  # Consume trailing command expression ")"

        return self