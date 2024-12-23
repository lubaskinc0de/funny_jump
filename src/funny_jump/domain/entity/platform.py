from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Platform(Protocol):
    center_x: int
    center_y: int
    width: int
    height: int

    @abstractmethod
    def on_collide(self) -> None: ...


@dataclass(slots=True)
class BasicPlatform(Platform):
    center_x: int = 0
    center_y: int = 0
    width: int = 0
    height: int = 0

    def on_collide(self) -> None:
        return None
