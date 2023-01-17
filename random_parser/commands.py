

# TODO: Decide if this should be separate, or kept with the parser class.
from dataclasses import dataclass
import logging
import random
from typing import Callable, Iterable, Union


class Commands():

    @dataclass
    class ArgumentFragment():
        # TODO: Consider making a top-level class that can parse itself.
        text: str

    @dataclass
    class Command():
        def __init__(
                self, name: str, arg_types: Iterable[Union[int, str, float]],
                rtype: Union[int, str],
                evaluator: Callable):
            self.name = name
            self.arg_types = arg_types
            self.type = rtype
            self.evaluate = self.make_evaluator(evaluator)

        def make_evaluator(self, evaluator):
            def evaluate(args):
                logging.debug(f'Evaluating function {self.name} with args {args}')
                args = list(map(lambda t, a: t(a), self.arg_types, args))
                result = evaluator(args)
                return self.type(result)
            return evaluate


    CONSTANT = Command('constant', [str], str, lambda l: l[0])
    COW = Command('cow', [], str, lambda _: "MOOOOOO")
    RANDOM = Command('random', [int, int], int, lambda l: random.randint(l[0], l[1]))
    GAUSS = Command('gauss', [float, float], int, lambda l: random.gauss(l[0], l[1]))
    GAMMA = Command('gamma', [float, float], int, lambda l: random.gammavariate(l[0], l[1]))
    BETA = Command('beta', [float, float], int, lambda l: random.betavariate(l[0], l[1]))
    ICONSTANT = Command('iconstant', [int], int, lambda l: l[0])

    COMMANDS = {
        command.name: command for command in [
            CONSTANT,
            COW,
            RANDOM,
            GAUSS,
            GAMMA,
            BETA,
            ICONSTANT,
        ]
    }
