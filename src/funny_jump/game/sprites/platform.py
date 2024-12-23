from typing import Protocol

from pygame.rect import Rect, RectType

from funny_jump.domain.entity.platform import Platform


class PlatformSprite(Protocol):
    rect: Rect | RectType
    platform: Platform
