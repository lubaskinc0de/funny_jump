from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity


class Platform(Protocol):
    velocity: Velocity
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
    is_alive: bool = True

    def on_collide(self) -> None:
        return None

    def death(self) -> None:
        self.is_alive = False

    def update(self) -> None:
        if self.bounds.center_y > (self.screen_h + 100):
            self.death()


class MobilePlatform(Platform):
    slots = (
        "screen_h",
        "screen_w",
        "velocity",
        "bounds",
        "is_alive",
        "default_center_x",
    )
    def __init__(
        self,
        screen_h: int,
        screen_w: int,
        velocity: Velocity,
        bounds: Bounds,
        is_alive: bool = True,
        ) -> None:
        self.screen_h = screen_h
        self.screen_w = screen_w
        self.velocity= velocity
        self.bounds = bounds
        self.is_alive = is_alive
        self.default_center_x: int = bounds.center_x

    def side_move(self) -> None:
        platform_shift = round(self.velocity.x * self.velocity.direction_x)

        if (
            abs(self.bounds.center_x - self.default_center_x + platform_shift) >= self.screen_w // 2
            or self.screen_w * 0.1 > self.bounds.center_x + platform_shift
            or self.bounds.center_x + platform_shift > self.screen_w * 0.9
            ):
            self.velocity.direction_x = -self.velocity.direction_x
            platform_shift = -platform_shift

        self.bounds.center_x += platform_shift

    def on_collide(self) -> None:
        return None

    def death(self) -> None:
        self.is_alive = False

    def update(self) -> None:
        self.side_move()

        if self.bounds.center_y > (self.screen_h + 100):
            self.death()
