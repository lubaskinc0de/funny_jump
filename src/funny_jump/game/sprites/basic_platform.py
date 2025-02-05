from __future__ import annotations

from pathlib import Path

import pygame

from funny_jump.domain.entity.platform import Platform
from funny_jump.game.sprites.platform import PlatformSprite


class BasicPlatformSprite(PlatformSprite):
    def __init__(
        self,
        platform: Platform,
        image: Path,
        size: tuple[int, int],
    ) -> None:
        super().__init__()

        img = self.load_img(image, size)
        self.set_img(img)
        self.rect = self.image.get_rect()

        self.platform = platform
        self.platform.bounds.height = self.rect.height
        self.platform.bounds.width = self.rect.width

    def load_img(self, path: Path, size: tuple[int, int]) -> pygame.Surface:
        img = pygame.image.load(path).convert_alpha()
        img.set_colorkey("black")

        bounding_rect = img.get_bounding_rect()
        img = img.subsurface(bounding_rect)

        img = pygame.transform.scale(img, size)

        return img

    def set_img(self, img: pygame.Surface) -> None:
        self.image = img

    def set_position_by_platform(self) -> None:
        self.rect.center = (round(self.platform.bounds.center_x), round(self.platform.bounds.center_y))

    def set_position(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
        self.platform.bounds.center_x = self.rect.centerx
        self.platform.bounds.center_y = self.rect.centery

    def update(self, delta: float) -> None:
        self.platform.update()
        self.set_position_by_platform()
