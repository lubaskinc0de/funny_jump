from pathlib import Path

import pygame
from pygame.sprite import Sprite

from funny_jump.domain.entity.platform import BasicPlatform
from funny_jump.game.sprites.platform import PlatformSprite


class BasicPlatformSprite(Sprite, PlatformSprite):
    def __init__(
        self,
        platform: BasicPlatform,
        image: Path,
        size: tuple[int, int],
    ) -> None:
        super().__init__()

        img = pygame.image.load(image).convert_alpha()
        img.set_colorkey("black")

        bounding_rect = img.get_bounding_rect()
        img = img.subsurface(bounding_rect)

        img = pygame.transform.scale(img, size)

        self.image = img
        self.rect = self.image.get_rect()
        self.platform = platform

    def set_pos(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
        self.platform.center_x = self.rect.centerx
        self.platform.center_y = self.rect.centery

    def update(self) -> None: ...
