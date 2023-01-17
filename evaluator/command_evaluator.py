
import logging
from random_parser.command_expression_parser import CommandExpressionParser
from random_parser.commands import Commands

class CommandEvaluator():

    def __init__(self, command_parser: CommandExpressionParser):
        self.command = command_parser.command  # Commands.Command
        self.arguments = command_parser.arguments  # Iterable[Commands.ArgumentParser]

    def evaluate_arguments(self, arguments):
        evaluated_arguments = []
        for argument in arguments:
            if isinstance(argument, Commands.ArgumentFragment):
                evaluated_arguments.append(argument.text)
            elif isinstance(argument, CommandExpressionParser):
                nested_command_evaluator = CommandEvaluator(argument)
                evaluated_arguments.append(nested_command_evaluator.evaluate_command())
            else:
                raise ValueError(f'Got invalid argument: {self.argument}')
        return evaluated_arguments

    def evaluate_command(self):
        logging.info(f'Evaluating command {self.command}({self.arguments})')
        if self.command == Commands.CONSTANT:
            return self.evaluate_arguments(self.arguments)[0]
        else:
            raise ValueError(f'Got invalid command: {self.command}({self.arguments})')