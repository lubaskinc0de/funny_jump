from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol

from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity

MAX_TOUCHES = 2


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


class BasePlatform(ABC, Platform):
    is_alive: bool
    bounds: Bounds
    screen_h: int

    def on_collide(self) -> None:
        return None

    def death(self) -> None:
        self.is_alive = False

    def update(self) -> None:
        if self.bounds.center_y > (self.screen_h + 100):
            self.death()


@dataclass(slots=True)
class BasicPlatform(BasePlatform):
    screen_h: int
    velocity: Velocity
    bounds: Bounds
    is_alive: bool = True


class MobilePlatform(BasePlatform):
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
        *,
        is_alive: bool = True,
    ) -> None:
        self.screen_h = screen_h
        self.screen_w = screen_w
        self.velocity = velocity
        self.bounds = bounds
        self.is_alive = is_alive
        self.default_center_x: int = bounds.center_x
        self.delta: float = 0.0

    def side_move(self) -> None:
        platform_shift = round(self.velocity.x * self.velocity.direction_x * self.delta)

        if (
            abs(self.bounds.center_x - self.default_center_x + platform_shift) >= self.screen_w // 2
            or self.screen_w * 0.1 > self.bounds.center_x + platform_shift
            or self.bounds.center_x + platform_shift > self.screen_w * 0.9
        ):
            self.velocity.direction_x = -self.velocity.direction_x
            platform_shift = -platform_shift

        self.bounds.center_x += platform_shift

    def set_delta(self, delta: float) -> None:
        self.delta = delta

    def update(self) -> None:
        self.side_move()
        super().update()


@dataclass
class OnetimePlatform(BasicPlatform):
    collision_counter: int = field(init=False, default=0)

    @property
    def is_last_hit(self) -> bool:
        return self.collision_counter >= 1

    def on_collide(self) -> None:
        super().on_collide()
        self.collision_counter += 1

    def update(self) -> None:
        super().update()

        if self.collision_counter >= MAX_TOUCHES:
            self.death()


class PlatformType(Enum):
    BASIC = auto()
    MOBILE = auto()
    ONETIME = auto()
