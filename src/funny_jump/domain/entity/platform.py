from funny_jump.domain.value_object.velocity import Velocity
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.entity.player import GRAVITY, JUMP_STRENGTH

from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

SPEED = 10 * 60


class Platform(Protocol):
    center_x: int
    center_y: int

    @abstractmethod
    def on_collide(self) -> None:...
    
    @abstractmethod
    def update(self) -> None: ...
    
    @abstractmethod
    def death(self) -> None: ...
    
    @abstractmethod
    def move_down(self) -> None: ...
    

@dataclass(slots=True)
class BasicPlatform(Platform):
    screen_h: int
    velocity: Velocity
    bounds: Bounds
    speed: int = SPEED
    is_alive: bool = True
    delta: float = 0.0
    
    def set_delta(self, delta: float) -> None:
        self.delta = delta
    
    def on_collide(self) -> None:
        return None

    def death(self) -> None:
        self.is_alive = False
        
    def move_down(self) -> None:
        self.velocity.y += SPEED * self.delta
        self.bounds.center_y += round(self.velocity.y * self.delta)
    
    def update(self) -> None:
        self.bounds.center_y = max(self.bounds.center_y, 0)
        
        if self.bounds.center_y > (self.screen_h + 100):
            self.death()