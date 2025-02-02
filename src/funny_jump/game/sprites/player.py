from dataclasses import dataclass
from pathlib import Path

import pygame
from pygame.key import ScancodeWrapper

from funny_jump.domain.entity.player import Player
from funny_jump.engine.animation.animation_manager import AnimationId, AnimationManager
from funny_jump.engine.sprite import BoundedSprite

HOP_ANIMATION_ID = AnimationId("PLAYER_HOP")


@dataclass(slots=True, frozen=True)
class PlayerSounds:
    jump: pygame.mixer.Sound


class PlayerSprite(BoundedSprite):
    def __init__(
        self,
        player: Player,
        image: Path,
        size: tuple[int, int],
        animation_manager: AnimationManager,
        sounds: PlayerSounds,
    ) -> None:
        super().__init__()

        img = pygame.image.load(image)
        self.facing_right = True
        self.size = size
        self.animation_manager = animation_manager

        self.set_new_image(img)
        self.static_img = self.original_image

        self.rect = self.image.get_rect()
        self.prev_pos = self.rect

        self.player = player
        self.player.bounds.height = self.rect.height
        self.player.bounds.width = self.rect.width

        self.set_position(self.rect.centerx, self.rect.centery)
        self.delta = 0.0
        self.sounds = sounds

    def animation_end(self) -> None:
        self.set_new_image(self.static_img)

    def set_new_image(self, new_img: pygame.Surface) -> None:
        new_img = new_img.convert_alpha()
        new_img.set_colorkey("black")

        bounding_rect = new_img.get_bounding_rect()
        img = new_img.subsurface(bounding_rect)
        img = pygame.transform.scale(img, self.size)

        self.original_image = img
        self.image = self.original_image

        if not self.facing_right:
            self.image = pygame.transform.flip(
                self.image,
                flip_x=True,
                flip_y=False,
            )

    def set_position(self, x: float, y: float) -> None:
        self.rect.center = (round(x), round(y))

        self.player.bounds.center_x = self.rect.centerx
        self.player.bounds.center_y = self.rect.centery

    def set_position_by_player(self) -> None:
        self.rect.center = (round(self.player.bounds.center_x), round(self.player.bounds.center_y))

    def update(self, delta: float) -> None:
        self.prev_pos = self.rect.copy()
        self.delta = delta

        keys_pressed = pygame.key.get_pressed()
        self.handle_keys_down(keys_pressed)

        self.jump()
        self.player.set_delta(delta)
        self.player.update()
        self.set_position_by_player()
        self.animation_manager.update(delta)

    def move_left(self) -> None:
        if self.facing_right:
            self.facing_right = False
            self.image = pygame.transform.flip(
                self.image,
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
        if self.player.jump():
            self.animation_manager.apply(self, HOP_ANIMATION_ID)
            self.sounds.jump.play()

    def handle_keys_down(self, keys_pressed: ScancodeWrapper) -> None:
        if keys_pressed[pygame.K_LEFT]:
            self.move_left()
        elif keys_pressed[pygame.K_RIGHT]:
            self.move_right()
