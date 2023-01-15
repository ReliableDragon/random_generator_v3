import logging
from typing import Iterable


from random_parser.base_parser import BaseParser
from random_parser.subchoice_parser import SubchoiceParser

class ChoiceBodyParser(BaseParser):

    def __init__(self, filename: str, lines: Iterable[str], line_num: int):
        super().__init__(filename, lines, line_num)
        self.text_fragments = []
        self.subchoices = []

    def parse(self):
        assert self.line(), self.err_msg('Empty choice body')
        choice_header = self.use_line()
        self.text_fragments = choice_header.split('$')
        num_fragments = len(self.text_fragments) - 1  # Subtract one to avoid a fencepost error.

        fragment_num = 1
        while fragment_num <= num_fragments:
            logging.info(f'Beginning parse of fragment #{fragment_num} of {num_fragments}')
            subchoice = SubchoiceParser(self.filename, self.lines, self.line_num, fragment_num, choice_header)
            subchoice.parse()
            self.subchoices.append(subchoice)
            self.line_num = subchoice.line_num
            fragment_num += 1
            logging.info(f'Finished parsing fragment: {subchoice}')

        return self

    def length(self):
        return len(self.subchoices)