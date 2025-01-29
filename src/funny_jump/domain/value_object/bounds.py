from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Bounds:
    center_x: int = 0
    center_y: int = 0
    width: int = 0
    height: int = 0

    @property
    def bottom(self) -> int:
        return self.center_y + self.height // 2

    @property
    def top(self) -> int:
        return self.center_y - self.height // 2

    def __eq__(self, other: "Bounds | Any") -> bool:  # noqa: ANN401
        if not isinstance(other, Bounds):
            return False

        return (
            self.center_x == other.center_x
            and self.center_y == other.center_y
            and self.width == other.width
            and self.height == other.height
        )
