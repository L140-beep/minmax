from dataclasses import dataclass


@dataclass
class Point():
    x: int
    y: int

    def __repr__(self) -> str:
        return f'Point({self.x, self.y})'

    def __str__(self) -> str:
        return f'Point({self.x, self.y})'
