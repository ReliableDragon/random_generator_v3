import argparse
import logging
import os
import sys

from evaluator.generator_evaluator import GeneratorEvaluator
from random_parser.parser import Parser

from typing import Any, Iterable, Optional, Union

#  (:%(funcName)s)
logging.basicConfig(format='> %(filename)s:%(lineno)d %(message)s', level=logging.INFO)
logging.getLogger().setLevel(logging.WARNING)

def parse_args() -> Iterable[Any]:
    parser = argparse.ArgumentParser(
        prog='RandomGenerator',
        description='Generate randomness!',
    )
    parser.add_argument('-f', '--filter', nargs='?')
    parser.add_argument('-g', '--generators', nargs='?')
    parser.add_argument('-i', '--inputs', nargs='?')
    args = parser.parse_args()
    return args

def get_choice() -> Union[int, str]:
    """Gets the 0-indexed choice of item to generate."""
    while True:
        choice = input('Choose an item to generate: ')
        if choice.lower().startswith('exit'):
            return 'exit'
        try:
            choice = int(choice)
            return choice - 1
        except:
            pass

def repl(generator: GeneratorEvaluator):
    while True:
        generations = generator.get_available_generations()
        for i, generation in enumerate(generations):
            print(f'{i+1}: {generation}')
        choice = get_choice()
        if choice == 'exit':
            break
        generated = generator.evaluate(choice)
        print(generated)

def run(args: argparse.Namespace) -> None:
        """Runs the generator.

        Args:
        args: Parsed command line arguments."""
        print('Running the random choice generator!')
        parser = Parser(args.generators, args.inputs)
        parser.parse(args.filter)
        generator = GeneratorEvaluator(parser)
        repl(generator)


if __name__ == '__main__':
    args = parse_args()
    run(args)
