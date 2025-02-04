from pathlib import Path

from funny_jump.domain.entity.platform import MobilePlatform
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite


class MobilePlatformSprite(BasicPlatformSprite):
    def __init__(
        self,
        platform: MobilePlatform,
        image: Path,
        size: tuple[int, int],
    ) -> None:
        super().__init__(
            platform=platform,
            image=image,
            size=size,
        )
        self.platform: MobilePlatform = platform

    def update(self, delta: float) -> None:
        self.delta = delta
        self.platform.set_delta(delta)
        self.platform.update()
        self.set_position_by_platform()
