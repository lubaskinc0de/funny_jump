from pathlib import Path

import pygame
from pygame.key import ScancodeWrapper
from pygame.sprite import Sprite

from funny_jump.domain.entity.player import Player


class PlayerSprite(Sprite):
    def __init__(
        self,
        player: Player,
        image: Path,
        size: tuple[int, int],
    ) -> None:
        super().__init__()

        img = pygame.image.load(image).convert_alpha()
        img.set_colorkey("black")

        bounding_rect = img.get_bounding_rect()
        img = img.subsurface(bounding_rect)
        img = pygame.transform.scale(img, size)

        self.original_image = self.image = img
        self.rect = self.image.get_rect()

        self.player = player
        self.player.bounds.height = self.rect.height
        self.player.bounds.width = self.rect.width

        self.facing_right = True
        self.set_position(self.rect.centerx, self.rect.centery)
        self.delta = 0.0

    def set_position(self, x: float, y: float) -> None:
        self.rect.center = (round(x), round(y))

        self.player.bounds.center_x = self.rect.centerx
        self.player.bounds.center_y = self.rect.centery

    def set_position_by_player(self) -> None:
        self.rect.center = (round(self.player.bounds.center_x), round(self.player.bounds.center_y))

    def update(self, delta: float) -> None:
        self.delta = delta

        keys_pressed = pygame.key.get_pressed()
        self.handle_keys_down(keys_pressed)

        self.player.set_delta(delta)
        self.player.update()
        self.set_position_by_player()

    def move_left(self) -> None:
        if self.facing_right:
            self.facing_right = False
            self.image = pygame.transform.flip(
                self.original_image,
                flip_x=True,
                flip_y=False,
            )
        self.player.move_left()

    def move_right(self) -> None:
        if not self.facing_right:
            self.facing_right = True
            self.image = self.original_image
        self.player.move_right()

    def jump(self) -> None:
        self.player.jump()

    def handle_keys_down(self, keys_pressed: ScancodeWrapper) -> None:
        if keys_pressed[pygame.K_LEFT]:
            self.move_left()
        elif keys_pressed[pygame.K_RIGHT]:
            self.move_right()

        if keys_pressed[pygame.K_SPACE]:
            self.jump()
