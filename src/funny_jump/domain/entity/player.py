from dataclasses import dataclass

SPEED = 8
JUMP_STRENGTH = 14
GRAVITY = 0.7


@dataclass(slots=True)
class Player:
    screen_w: int
    screen_h: int
    center_x: float = 0
    center_y: float = 0
    bottom: int = 0
    velocity_y: float = 0
    velocity_x: float = 0
    jump_strength: int = JUMP_STRENGTH
    speed: int = SPEED
    on_ground: bool = False
    health: int = 100

    def move_left(self) -> None:
        self.velocity_x -= self.speed

    def move_right(self) -> None:
        self.velocity_x += self.speed

    def jump(self) -> None:
        self.velocity_y = 0
        self.velocity_y -= JUMP_STRENGTH

    def _process_gravity(self) -> None:
        self.velocity_y += GRAVITY

    def process_physics(self) -> None:
        if not self.on_ground:
            self._process_gravity()

    def death(self) -> None:
        self.center_y = self.screen_h
        self.health = 0

    def get_on_ground(self) -> None:
        self.velocity_y = 0
        self.on_ground = True

    def left_from_ground(self) -> None:
        self.on_ground = False

    def update(self) -> None:
        self.process_physics()

        self.center_y += self.velocity_y
        self.center_x += self.velocity_x
        self.center_x = int(self.center_x)
        self.center_y = int(self.center_y)

        self.center_x %= self.screen_w

        self.center_y = max(self.center_y, 0)
        if self.center_y > self.screen_h:
            self.death()

        self.velocity_x = 0
