import os
import random

from typing import IO, Iterable, Optional, TextIO
from evaluator.subchoice_evaluator import SubchoiceEvaluator

from random_parser.parser import Parser
from random_parser.subchoice_parser import SubchoiceParser

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

    def evaluate_subchoice(self, subchoice: SubchoiceParser):
        return SubchoiceEvaluator.randomly_generate_subchoice(subchoice)

    def evaluate(self, choice: int = 0) -> str:
        choice_body = self.parser.top_level_generators[choice].get_body()
        generation = ''
        i = 0
        while i < choice_body.length():
            generation += choice_body.text_fragments[i]
            generation += self.evaluate_subchoice(choice_body.subchoices[i])
            i += 1

        generation += choice_body.text_fragments[i]
        return generation
