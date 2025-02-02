from funny_jump.domain.entity.platform import Platform
from funny_jump.engine.sprite import BoundedSprite


class PlatformSprite(BoundedSprite):
    platform: Platform
