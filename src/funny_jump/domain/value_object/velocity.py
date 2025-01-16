from dataclasses import dataclass
from typing import Literal


@dataclass(slots=True)
class Velocity:
    x: float = 0
    y: float = 0
    direction_x: Literal[1, -1, 0] = 0
