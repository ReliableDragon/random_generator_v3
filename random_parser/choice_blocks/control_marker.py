

from dataclasses import dataclass


@dataclass
class ControlMarker():
    marker: str
    index: int

    def __str__(self):
        return f'({self.marker}, {self.index})'