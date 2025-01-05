from dataclasses import dataclass

from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity

SPEED = 8*60
JUMP_STRENGTH = 16*60
GRAVITY = 42*60


@dataclass(slots=True)
class Player:
    screen_w: int
    screen_h: int
    bounds: Bounds
    velocity: Velocity
    jump_strength: int = JUMP_STRENGTH
    speed: int = SPEED
    on_ground: bool = False
    health: int = 100
    is_jumping: bool = False
    delta: float = 0.0
    gravity: float = GRAVITY

    def set_delta(self, delta: float) -> None:
        """Must be called on every frame."""
        self.delta = delta

    def move_left(self) -> None:
        self.velocity.x = -self.speed

    def move_right(self) -> None:
        self.velocity.x = self.speed

    def jump(self) -> None:
        if self.is_jumping:
            return

        self.velocity.y = -self.jump_strength
        self.is_jumping = True

    def _process_gravity(self) -> None:
        self.velocity.y += self.gravity * self.delta

    def process_physics(self) -> None:
        if not self.on_ground:
            self._process_gravity()

        if self.velocity.y > 0 and self.is_jumping:
            self.is_jumping = False

        self.bounds.center_y += round(self.velocity.y * self.delta)
        self.bounds.center_x += round(self.velocity.x * self.delta)

        self.velocity.x = 0

    def death(self) -> None:
        self.bounds.center_y = self.screen_h
        self.health = 0

    def get_on_ground(self) -> None:
        self.velocity.y = 0
        self.on_ground = True

    def left_from_ground(self) -> None:
        self.on_ground = False

    def update(self) -> None:
        self.process_physics()

        self.bounds.center_x %= self.screen_w

        self.bounds.bottom = min(self.screen_h, self.bounds.bottom)
        print(self.bounds.bottom)
