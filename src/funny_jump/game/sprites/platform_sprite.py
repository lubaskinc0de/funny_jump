from abc import ABC, abstractmethod

from funny_jump.domain.entity.platform_entity import Platform
from funny_jump.engine.sprite import BoundedSprite


class PlatformSprite(BoundedSprite, ABC):
    platform: Platform

    @abstractmethod
    def set_position(self, x: int, y: int) -> None: ...
