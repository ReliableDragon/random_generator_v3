import logging
from typing import TYPE_CHECKING, Iterable
from random_parser.constants import WEIGHTED_CHOICE_OPEN_DELIMITER, WEIGHTED_CHOICE_CLOSE_DELIMITER, WEIGHTED_CHOICE_END, WEIGHTED_CHOICE_SEPARATOR
from random_parser.context import Context
from random_parser.token_parser import TokenParser
from random_parser.choice_blocks.choice_block import ChoiceBlockParser
from random_parser.commands.command import CommandParser

class WeightedChoiceWeightParser(TokenParser):

    def __init__(self, parser: TokenParser):
        super().__init__(parser)
        self.weight = None  # Union[TextFragmentParser, ChoiceBlockParser]
        self.is_command_weight = False

    def get_weight(self, context: Context):
        if isinstance(self.weight, int):
            return self.weight
        elif isinstance(self.weight, CommandParser):
            return self.weight.evaluate(context)
        else:
            raise ValueError(f'Got invalid weight: {self.weight}')

    def is_next_char_valid(self):
        if self.is_eol():
            return False
        if self.char() == WEIGHTED_CHOICE_SEPARATOR:
            return False
        return True

    def parse(self):
        assert self.char().isdecimal() or self.char() == WEIGHTED_CHOICE_OPEN_DELIMITER, self.err_msg(
            f'Expected either integer or "{WEIGHTED_CHOICE_OPEN_DELIMITER}" to start weight, but '
            f'instead got {self.char()} at beginning of {self.context()}')
        if self.char() == WEIGHTED_CHOICE_OPEN_DELIMITER:
            self.use_char()  # Consume leading "["
            self.is_command_weight = True
            weight_command = CommandParser(self, is_integer=True)
            weight_command.parse()
            self.sync(weight_command)
            assert self.char() == WEIGHTED_CHOICE_CLOSE_DELIMITER, self.err_msg(f'Got invlid end to weight command')
            self.use_char()  # Consume trailing "]"
            self.weight = weight_command
        else:
            token = ''
            while self.is_next_char_valid():
                token += self.use_char()
            assert token.isdecimal(), self.err_msg(f'Got invalid integer weight: {token}')
            self.weight = int(token)

        return self