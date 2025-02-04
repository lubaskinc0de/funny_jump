from dataclasses import dataclass, field

from funny_jump.domain.entity.platform import Platform
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity

SPEED = 8 * 60
JUMP_STRENGTH = 14 * 60
GRAVITY = 42 * 60


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
    staying_at: Platform | None = field(init=False)

    def set_delta(self, delta: float) -> None:
        """Must be called on every frame."""
        self.delta = delta

    def move_left(self) -> None:
        self.velocity.direction_x = -1

    def move_right(self) -> None:
        self.velocity.direction_x = 1

    def jump(self) -> bool:
        if self.is_jumping or not self.on_ground:
            return False

        self.velocity.y = -self.jump_strength
        self.is_jumping = True
        return True

    def _process_gravity(self) -> None:
        self.velocity.y += self.gravity * self.delta

    def process_physics(self) -> None:
        if not self.on_ground:
            self._process_gravity()

        if self.velocity.y > 0 and self.is_jumping:
            self.is_jumping = False

        self.bounds.center_y += round(self.velocity.y * self.delta)
        self.bounds.center_x += round(self.speed * self.delta * self.velocity.direction_x)

        self.velocity.direction_x = 0

    def death(self) -> None:
        self.health = 0

    def get_on_ground(self, platform: Platform) -> None:
        self.velocity.y = 0
        self.on_ground = True
        self.staying_at = platform

    def left_from_ground(self) -> None:
        self.on_ground = False
        self.staying_at = None

    @property
    def max_jump_height(self) -> int:
        return round((self.jump_strength**2) / (2 * GRAVITY))

    @property
    def max_horizontal_jump(self) -> int:
        jump_time = (2 * self.jump_strength) / self.gravity
        max_distance = self.speed * jump_time

        return round(max_distance)

    def update(self) -> None:
        self.process_physics()

        self.bounds.center_x %= self.screen_w

        if self.bounds.bottom >= self.screen_h:
            self.bounds.center_y = self.screen_h - self.bounds.height // 2
            self.death()
        if self.bounds.top <= 0:
            self.bounds.center_y = self.bounds.height // 2
