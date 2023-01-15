
from typing import Iterable


def generate_err_msg(filename: str, lines: Iterable[str]):
    return lambda line_num, error: f'{filename}, line {line_num+1}> {error}: "{lines[line_num]}"'
