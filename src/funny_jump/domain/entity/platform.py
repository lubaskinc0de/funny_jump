from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Platform(Protocol):
    center_x: int
    center_y: int

    @abstractmethod
    def on_collide(self) -> None:...
    
    def update(self) -> None: ...
    
    def death(self) -> None: ...
    
    def move_down(self) -> None: ...
    

@dataclass(slots=True)
class BasicPlatform(Platform):
    screen_h: int
    center_x: int = 0
    center_y: int = 0
    is_alive: bool = True
    speed: int = 8
    
    def on_collide(self) -> None:
        return None

    def death(self) -> None:
        self.is_alive = False
        
    def move_down(self) -> None:
        self.center_y += self.speed
    
    def update(self) -> None:
        self.center_y = int(self.center_y)

        self.center_x %= self.screen_w

        self.center_y = max(self.center_y, 0)
        
        if self.center_y > (self.screen_h + 50):
            self.death()