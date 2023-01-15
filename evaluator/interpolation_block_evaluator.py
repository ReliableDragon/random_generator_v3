
import random


class InterpolationBlockEvaluator():

    def randomly_generate_weighted_choice(subchoice):
        total_weight = sum(subchoice.weights)
        threshold = random.randint(1, total_weight)
        i = -1  # Start at -1 to ensure loop condition evaluates properly at i=0.
        weight_sum = 0
        while weight_sum < threshold:
            i += 1
            weight_sum += subchoice.weights[i]
        choice = subchoice.choices[i]
        return choice