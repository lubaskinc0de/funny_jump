from random import randint
from typing import Literal

import pygame.sprite

from funny_jump.domain.entity.platform import BasicPlatform, MobilePlatform
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite
from funny_jump.game.sprites.mobile_platform import MobilePlatformSprite
from funny_jump.game.sprites.player import PlayerSprite

BASIC_PLATFORM_SIZE = (100, 30)
MAX_PLATFORM_HEIGHT = -200


class PlatformManager:
    def __init__(
        self,
        platforms: pygame.sprite.Group,  # type: ignore
        screen_w: int,
        screen_h: int,
        player_sprite: PlayerSprite,
        asset_manager: AssetManager[Asset],
        platform_moving_speed: float = 0,
    ) -> None:
        self.player_sprite = player_sprite
        self.platforms = platforms
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.asset_manager = asset_manager
        self.platform_spawn_height = self.screen_h // 2
        self.platform_moving_speed = platform_moving_speed
        self.delta: float = 0.0
        self.spawn_initial_platforms()

    def get_highest_platform(self) -> BasicPlatformSprite:
        """Возвращает объект самой высокой платформы."""
        sprites: list[BasicPlatformSprite] = self.platforms.sprites()
        highest_platform_sprite = sprites[0]

        for platform_sprite in sprites[1:]:
            if platform_sprite.platform.bounds.center_y < highest_platform_sprite.platform.bounds.center_y:
                highest_platform_sprite = platform_sprite

        return highest_platform_sprite

    def spawn_platform(self, center_x: int, center_y: int, can_move: bool = False) -> None:
        """Создает спрайт платформы и добавляет его в группу всех платформ."""
        if not can_move:
            basic_platform = BasicPlatform(
                screen_h=self.screen_h,
                velocity=Velocity(),
                bounds=Bounds(center_x, center_y),
            )
            platform_sprite = BasicPlatformSprite(
                platform=basic_platform,
                image=self.asset_manager.get_asset_path(Asset.PLATFORM_SPRITE),
                size=BASIC_PLATFORM_SIZE,
            )
        else:
            platform_x_speed = BASIC_PLATFORM_SIZE[0] * self.platform_moving_speed * 3.5
            platform_x_direction: Literal[-1, 1] = 1 if randint(-2, 1) >= 0 else -1
            moving_platform = MobilePlatform(
                screen_h=self.screen_h,
                screen_w=self.screen_w,
                velocity=Velocity(
                    x=platform_x_speed,
                    direction_x=platform_x_direction,
                    ),
                bounds=Bounds(center_x, center_y),
            )

            platform_sprite = MobilePlatformSprite(
                platform=moving_platform,
                image=self.asset_manager.get_asset_path(Asset.MOBILE_PLATFORM_SPRITE),
                size=BASIC_PLATFORM_SIZE,
            )

        platform_sprite.set_position(center_x, center_y)
        self.platforms.add(platform_sprite)

    def is_overlapping(self, center_x: int, center_y: int) -> bool:
        """Проверяет не соприкасается ли платформа с уже существующими."""
        new_bounds = Bounds(center_x, center_y)

        for platform_sprite in self.platforms:
            existing_bounds = platform_sprite.platform.bounds

            if (
                new_bounds.center_x < existing_bounds.center_x + existing_bounds.width + randint(50, 200)
                and new_bounds.center_x + BASIC_PLATFORM_SIZE[0] > existing_bounds.center_x
                and new_bounds.center_y < existing_bounds.center_y + existing_bounds.height + randint(30, 70)
                and new_bounds.center_y + BASIC_PLATFORM_SIZE[1] > existing_bounds.center_y
            ):
                return True

        return False

    def calculate_new_platform_position(self) -> tuple[int, int]:
        """Вычисляет подходящую позицию для спавга платформы."""
        highest_platform = self.get_highest_platform()
        next_platform_interval_x = 0
        center_x = highest_platform.platform.bounds.center_x
        while True:
            next_platform_interval_x = BASIC_PLATFORM_SIZE[0] * randint(-3, 3)
            center_x = highest_platform.platform.bounds.center_x + next_platform_interval_x
            if (
                next_platform_interval_x != 0
                and BASIC_PLATFORM_SIZE[0] < center_x
                and center_x < self.screen_w * 0.9 - BASIC_PLATFORM_SIZE[0] // 2
            ):
                break

        next_platform_interval_y = self.player_sprite.player.max_jump_height
        center_y = highest_platform.platform.bounds.center_y - next_platform_interval_y
        return center_x, center_y

    def spawn_initial_platforms(self) -> None:
        """Спавнит начальные платформы. Исполняется при инициализации PlatformManager."""
        center_x = self.screen_w // 2
        center_y = self.screen_h - 200
        self.spawn_platform(center_x, center_y)
        for _ in range(7):
            while center_x == 0 or center_y == 0 or self.is_overlapping(center_x, center_y):
                center_x, center_y = self.calculate_new_platform_position()
            self.spawn_platform(center_x, center_y)

    def spawn_new_platform(self) -> None:
        """Используется для спавна новой платформы."""
        center_x = 0
        center_y = 0
        while center_x == 0 or center_y == 0 or self.is_overlapping(center_x, center_y):
            center_x, center_y = self.calculate_new_platform_position()

        platform_moves = False
        if self.platform_moving_speed:
            platform_moves = randint(1, 100) - self.platform_moving_speed * 5 <= 10

        self.spawn_platform(center_x, center_y, platform_moves)

    def update(self, delta: float) -> None:
        self.delta = delta
        for platform_sprite in self.platforms:
            if self.player_sprite.rect.centery <= self.platform_spawn_height:
                offset = (self.platform_spawn_height - self.player_sprite.rect.centery) * delta * 3
                platform_sprite.set_position(platform_sprite.rect.centerx, platform_sprite.rect.centery + offset)
                if self.get_highest_platform().rect.centery > MAX_PLATFORM_HEIGHT:
                    self.spawn_new_platform()
            platform_sprite.platform.velocity.y = 0
