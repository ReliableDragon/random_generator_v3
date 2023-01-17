import logging
import os
import random

from typing import IO, Iterable, Optional, TextIO
from evaluator.command_evaluator import CommandEvaluator
from evaluator.interpolation_block_evaluator import InterpolationBlockEvaluator
from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.command_expression_parser import CommandExpressionParser
from random_parser.constants import GENERATOR_PARSER, RESOURCE_PARSER
from random_parser.import_interpolation_token_parser import ImportInterpolationTokenParser
from random_parser.interpolation_token_parser import InterpolationTokenParser

from random_parser.parser import Parser
from random_parser.interpolation_block_parser import InterpolationBlockParser
from random_parser.text_fragment_parser import TextFragmentParser
from random_parser.resource_parser import ResourceParser

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

    def evaluate(self, choice: int = 0) -> str:
        generator = self.parser.top_level_generators[choice]
        print(f'Evaluating {generator.filename}')
        return self.evaluate_generator(generator)

    def evaluate_generator(self, generator):
        choice_block = generator.choice_block
        return self.evaluate_choice_block(choice_block)

    def evaluate_resource(self, resource: ResourceParser):
        interpolation_block = resource.interpolation_block
        return self.evaluate_interpolation_block(interpolation_block)

    def evaluate_choice_block(self, choice_block: ChoiceBlockParser):
        logging.debug(f'Evaluating choice block {choice_block.print(top_level=True)}')
        generation = ''
        i = 0
        choice_expression = choice_block.choice_expression_parser
        for fragment in choice_expression.fragments:
            if isinstance(fragment, TextFragmentParser):
                generation += self.evaluate_text_fragment(fragment)
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

    def evaluate_interpolation_block(self, interpolation_block: InterpolationBlockParser):
        logging.debug(f'Evaluating interpolation block {interpolation_block}')
        choice = InterpolationBlockEvaluator.randomly_generate_weighted_choice(interpolation_block)
        if isinstance(choice, TextFragmentParser):
            return self.evaluate_text_fragment(choice)
        elif isinstance(choice, ChoiceBlockParser):
            return self.evaluate_choice_block(choice)
        else:
            raise ValueError(f'Got invalid choice in interpolation block: {choice}')

    def evaluate_text_fragment(self, text_fragment: TextFragmentParser):
        logging.debug(f'Evaluating text fragment {text_fragment}')
        generation = ''
        i = 0
        for fragment in text_fragment.fragments:
            if isinstance(fragment, text_fragment.RawTextFragment):
                generation += fragment.text
            elif isinstance(fragment, CommandExpressionParser):
                generation += self.evaluate_command_expression(fragment)
            else:
                raise ValueError(f'Got invalid text fragment: {fragment}')
        return generation

    def evaluate_command_expression(self, command_parser: CommandExpressionParser):
        command_evaluator = CommandEvaluator(command_parser)
        command_result = command_evaluator.evaluate_command()
        logging.warning(f'Command result: {command_result}')
        return command_result