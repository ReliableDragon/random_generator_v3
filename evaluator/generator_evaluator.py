import logging
import os
import random

from typing import IO, Iterable, Optional, TextIO
from evaluator.interpolation_block_evaluator import InterpolationBlockEvaluator
from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.constants import GENERATOR_PARSER, RESOURCE_PARSER
from random_parser.import_interpolation_token_parser import ImportInterpolationTokenParser
from random_parser.interpolation_token_parser import InterpolationTokenParser

from random_parser.parser import Parser
from random_parser.interpolation_block_parser import InterpolationBlockParser

class GeneratorEvaluator():
    """Generates randomness!

    Attrributes:
    parser: The parser containing all the information about the parsed text files."""

    parser: Parser

    def __init__(self, parser: Parser):
        self.parser = parser
        self.imports_cache = parser.imports_cache
        logging.info(f'Imports cache: {self.imports_cache.list_imports()}')

    def get_available_generations(self, generator_filter: str = None) -> Iterable[str]:
        if not generator_filter:
            return [p.name for p in self.parser.top_level_generators]
        else:
            return [generator_filter] if generator_filter in self.parser.top_level_generators else []

    def evaluate_interpolation_block(self, subchoice: InterpolationBlockParser):
        logging.debug(f'Evaluating subchoice {subchoice}')
        choice = InterpolationBlockEvaluator.randomly_generate_weighted_choice(subchoice)
        if isinstance(choice, str):
            return choice
        else:
            return self.evaluate_choice_block(choice)

    def evaluate(self, choice: int = 0) -> str:
        generator = self.parser.top_level_generators[choice]
        return self.evaluate_generator(generator)

    def evaluate_generator(self, generator):
        choice_block = generator.choice_block
        return self.evaluate_choice_block(choice_block)

    def evaluate_resource(self, resource):
        interpolation_block = resource.interpolation_block
        return self.evaluate_interpolation_block(interpolation_block)

    def evaluate_choice_block(self, choice_block: ChoiceBlockParser):
        logging.debug(f'Evaluating choice block {choice_block.print(top_level=True)}')
        generation = ''
        i = 0
        choice_expression = choice_block.choice_expression_parser
        for fragment in choice_expression.fragments:
            # TODO: Have choice block put all elements into a single "fragments" list, then
            # process on this side what to do with them. Maybe also consider a choice_expression
            if isinstance(fragment, choice_expression.TextFragment):
                generation += fragment.text
            elif isinstance(fragment, ImportInterpolationTokenParser):
                import_handle = fragment.import_handle
                import_ = self.imports_cache.get(import_handle)
                if import_.parser_type == GENERATOR_PARSER:
                    generation += self.evaluate_generator(import_.parser)
                elif import_.parser_type == RESOURCE_PARSER:
                    generation += self.evaluate_resource(import_.parser)
                else:
                    raise ValueError(f'Got unsupported parser type: {import_.parser_type}')
            elif isinstance(fragment, InterpolationTokenParser):
                fragment_num = fragment.token_num
                generation += self.evaluate_interpolation_block(choice_block.interpolation_blocks[fragment_num])
            else:
                raise ValueError(f'Unsupported fragment received: {fragment}')

        return generation
