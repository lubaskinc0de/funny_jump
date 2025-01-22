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
        self.platform: BasicPlatform = platform
        self.platform.bounds.height = self.rect.height
        self.platform.bounds.width = self.rect.width

    def set_position_by_platform(self) -> None:
        self.rect.center = (round(self.platform.bounds.center_x), round(self.platform.bounds.center_y))
    
    def set_position(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
        
        self.platform.bounds.center_x = self.rect.centerx
        self.platform.bounds.center_y = self.rect.centery
        
    def move_down(self, speed_mult) -> None:
        self.platform.move_down(speed_mult=1)
    
    def update(self, delta: float) -> None:
        self.delta = delta
        
        self.platform.set_delta(delta)
        self.platform.update()
        self.set_position_by_platform()
        