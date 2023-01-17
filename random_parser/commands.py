

# TODO: Decide if this should be separate, or kept with the parser class.
from dataclasses import dataclass
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

    CONSTANT = Command('constant', 1)
    # RANDOM = 'random'
    # NORMAL = 'normal'
    # GAUSS = 'gauss'
    COMMANDS = {
        CONSTANT.name: CONSTANT
    }
