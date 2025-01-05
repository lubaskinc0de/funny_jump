from dataclasses import dataclass


@dataclass(slots=True)
class Bounds:
    x: int = 0
    y: int = 0
    center_x: int = 0
    center_y: int = 0
    top: int = 0
    left: int = 0
    right: int = 0
    bottom: int = 0
