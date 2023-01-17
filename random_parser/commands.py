

# TODO: Decide if this should be separate, or kept with the parser class.
from dataclasses import dataclass
import random
from typing import Callable


class Commands():

    @dataclass
    class ArgumentFragment():
        # TODO: Consider making a top-level class that can parse itself.
        text: str

    @dataclass
    class Command():
        # TODO: Consider making this a top-level class that can parse and evaluate itself.
        name: str
        num_args: int  # Possibly support variable arguments later
        evaluate: Callable

    CONSTANT = Command('constant', 1, lambda l: l[0])
    COW = Command('cow', 0, lambda _: "MOOOOOO")
    RANDOM = Command('random', 2, lambda l: random.randint(int(l[0]), int(l[1])))
    # NORMAL = 'normal'
    # GAUSS = 'gauss'
    COMMANDS = {
        CONSTANT.name: CONSTANT,
        RANDOM.name: RANDOM,
        COW.name: COW,
    }
