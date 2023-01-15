import os
import random

from typing import IO, Iterable, Optional, TextIO
from evaluator.interpolation_block_evaluator import InterpolationBlockEvaluator
from random_parser.choice_block_parser import ChoiceBlockParser

from random_parser.parser import Parser
from random_parser.interpolation_block_parser import InterpolationBlockParser

class GeneratorEvaluator():
    """Generates randomness!

    Attrributes:
    parser: The parser containing all the information about the parsed text files."""

    parser: Parser

    def __init__(self, parser: Parser):
        self.parser = parser

    def get_available_generations(self, generator_filter: str = None) -> Iterable[str]:
        if not generator_filter:
            return [p.name for p in self.parser.top_level_generators]
        else:
            return [generator_filter] if generator_filter in self.parser.top_level_generators else []

    def evaluate_subchoice(self, subchoice: InterpolationBlockParser):
        choice = InterpolationBlockEvaluator.randomly_generate_weighted_choice(subchoice)
        if isinstance(choice, str):
            return choice
        else:
            return self.evaluate_choice_block(choice)

    def evaluate(self, choice: int = 0) -> str:
        choice_block = self.parser.top_level_generators[choice].choice_block
        return self.evaluate_choice_block(choice_block)

    def evaluate_choice_block(self, choice_block: ChoiceBlockParser):
        generation = ''
        i = 0
        while i < choice_block.length():
            # TODO: Have choice block put all elements into a single "fragments" list, then
            # process on this side what to do with them. Maybe also consider a choice_expression
            # parser, if choice_block is getting too unwieldy. 
            generation += choice_block.text_fragments[i]
            generation += self.evaluate_subchoice(choice_block.subchoices[i])
            i += 1

        generation += choice_block.text_fragments[i]
        return generation
