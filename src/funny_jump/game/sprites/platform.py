from typing import Protocol

from funny_jump.domain.entity.platform import Platform


class PlatformSprite(Protocol):
    platform: Platform
