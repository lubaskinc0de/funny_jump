from pathlib import Path

from funny_jump.domain.entity.platform import OnetimePlatform
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite


class OnetimePlatformSprite(BasicPlatformSprite):
    def __init__(
        self,
        platform: OnetimePlatform,
        image: Path,
        image_red: Path,
        size: tuple[int, int],
    ) -> None:
        super().__init__(
            platform=platform,
            image=image,
            size=size,
        )
        self.platform: OnetimePlatform = platform
        self.image_red = self.load_img(image_red, size)

    def update(self, delta: float) -> None:
        super().update(delta)

        if self.platform.is_last_hit:
            self.set_img(self.image_red)
