import argparse
import logging
import os
import sys

from evaluator.generator_evaluator import GeneratorEvaluator
from random_parser.parser import Parser

from typing import Any, Iterable, Optional, Union

#  (:%(funcName)s)
logging.basicConfig(format='> %(filename)s:%(lineno)d %(message)s', level=logging.INFO)

def parse_args() -> Iterable[Any]:
    parser = argparse.ArgumentParser(
        prog='RandomGenerator',
        description='Generate randomness!',
    )
    parser.add_argument('-f', '--filter', nargs='?')
    parser.add_argument('-g', '--generators', nargs='?')
    parser.add_argument('-i', '--inputs', nargs='?')
    parser.add_argument('--info', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    return args

def get_choice(length) -> Union[int, str]:
    """Gets the 0-indexed choice of item to generate."""
    while True:
        choice = input('Choose an item to generate: ')
        if choice.lower().startswith('exit'):
            return 'exit'
        try:
            choice = int(choice) - 1  # Subtract 1 as users use 1-indexed values
            if choice >= length:
                print('Invalid choice!')
                continue
            return choice
        except:
            pass

def repl(parser: Parser):
    while True:
        generations = parser.get_available_generations()
        for i, generation in enumerate(generations):
            print(f'{i+1}: {generation}')  # Add 1 so users see 1-indexed values
        choice = get_choice(len(generations))
        if choice == 'exit':
            break
        generated = parser.evaluate(choice)
        print(generated + '\n\n')

def run(args: argparse.Namespace) -> None:
        """Runs the generator.

        Args:
        args: Parsed command line arguments."""
        print('Running the random choice generator!')
        parser = Parser(args.generators, args.inputs)
        parser.parse(args.filter)
        repl(parser)


if __name__ == '__main__':
    args = parse_args()
    logger = logging.getLogger()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.info:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    run(args)
