from dataclasses import dataclass


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
