from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity

SPEED = 18 * 60


class Platform(Protocol):
    bounds: Bounds
    is_alive: bool

    @abstractmethod
    def on_collide(self) -> None: ...

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def death(self) -> None: ...


@dataclass(slots=True)
class BasicPlatform(Platform):
    screen_h: int
    velocity: Velocity
    bounds: Bounds
    speed: int = SPEED
    is_alive: bool = True

    def on_collide(self) -> None:
        return None

    def death(self) -> None:
        self.is_alive = False

    def update(self) -> None:
        if self.bounds.center_y > (self.screen_h + 100):
            self.death()
