
import random
from typing import Union

from random_parser.interpolation_block_parser import InterpolationBlockParser
from random_parser.choice_block_parser import ChoiceBlockParser
from random_parser.text_fragment_parser import TextFragmentParser


class InterpolationBlockEvaluator():

    def randomly_generate_weighted_choice(interpolation_block: InterpolationBlockParser) -> Union[ChoiceBlockParser, TextFragmentParser]:
        total_weight= sum([wc.weight for wc in interpolation_block.weighted_choices])
        threshold= random.randint(1, total_weight)
        i= -1  # Start at -1 to ensure loop condition evaluates properly at i=0.
        weight_sum = 0
        while weight_sum < threshold:
            i += 1
            weight_sum += interpolation_block.weighted_choices[i].weight
        choice = interpolation_block.weighted_choices[i].choice_value
        return choice
