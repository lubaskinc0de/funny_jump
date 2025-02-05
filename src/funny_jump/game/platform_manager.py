import random
from random import randint
from typing import Literal

import pygame.sprite

from funny_jump.domain.entity.platform import BasicPlatform, MobilePlatform, OnetimePlatform, PlatformType
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.game.difficulty_parameters import DifficultyParameters
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite
from funny_jump.game.sprites.mobile_platform import MobilePlatformSprite
from funny_jump.game.sprites.onetime_platform import OnetimePlatformSprite
from funny_jump.game.sprites.player import PlayerSprite

BASIC_PLATFORM_SIZE = (100, 30)
MAX_PLATFORM_HEIGHT = -350
MAX_REMOVED_PLATFORMS_FOR_MOVING_OTHERS = 10
PLATFROM_Y_MOVE_MULTIPLIER = 1.5
PLATFORMS_COUNT_MULTIPLIER = 2
PLATFORM_SPAWN_DISTANCE_MULTIPLIER = 3
MINIMAL_SCREEN_DISTANCE = 0.9
PLATFORM_Y_MAX_SPAWN_INTERVAL = -72
PLATFORM_Y_MIN_SPAWN_INTERVAL = -10
FIRST_PLATFORM_SPAWN_Y = 200
Y_OFFSET_COEFFICIENT = 0.9
ADDITIONAL_Y_OFFSET = 0.03
SCORE_INCREASE = 1


class PlatformManager:
    def __init__(
        self,
        all_sprites: pygame.sprite.Group,  # type: ignore
        platforms: pygame.sprite.Group,  # type: ignore
        screen_w: int,
        screen_h: int,
        player_sprite: PlayerSprite,
        asset_manager: AssetManager[Asset],
        difficulty_params: DifficultyParameters,
    ) -> None:
        self.player_sprite = player_sprite
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.asset_manager = asset_manager
        self.platform_spawn_height = self.screen_h // 2
        self.difficulty_params = difficulty_params
        self.delta = 0.0
        self.removed_platforms = 0
        self.score = 0

        self.spawn_initial_platforms()

    def get_highest_platform(self) -> BasicPlatformSprite:
        sprites: list[BasicPlatformSprite] = self.platforms.sprites()
        highest_platform_sprite = sprites[0]

        for platform_sprite in sprites[1:]:
            if platform_sprite.platform.bounds.center_y < highest_platform_sprite.platform.bounds.center_y:
                highest_platform_sprite = platform_sprite

        return highest_platform_sprite

    def spawn_platform(
        self,
        center_x: int,
        center_y: int,
        platform_type: PlatformType = PlatformType.BASIC,
    ) -> None:
        if platform_type == PlatformType.BASIC:
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
        elif platform_type == PlatformType.MOBILE:
            platform_x_speed = BASIC_PLATFORM_SIZE[0] * self.difficulty_params.platform_x_moving_speed
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
        elif platform_type == PlatformType.ONETIME:
            onetime_platform = OnetimePlatform(
                screen_h=self.screen_h,
                velocity=Velocity(),
                bounds=Bounds(center_x, center_y),
            )
            platform_sprite = OnetimePlatformSprite(
                platform=onetime_platform,
                image=self.asset_manager.get_asset_path(Asset.ONETIME_PLATFORM),
                image_red=self.asset_manager.get_asset_path(Asset.ONETIME_PLATFORM_RED),
                size=BASIC_PLATFORM_SIZE,
            )

        platform_sprite.set_position(center_x, center_y)
        self.platforms.add(platform_sprite)

    def is_overlapping(self, center_x: int, center_y: int) -> bool:
        new_bounds = Bounds(center_x, center_y)

        for platform_sprite in self.platforms:
            existing_bounds = platform_sprite.platform.bounds

            if (
                new_bounds.center_x < existing_bounds.center_x + existing_bounds.width
                and new_bounds.center_x + BASIC_PLATFORM_SIZE[0] > existing_bounds.center_x
                and new_bounds.center_y < existing_bounds.center_y + existing_bounds.height
                and new_bounds.center_y + BASIC_PLATFORM_SIZE[1] > existing_bounds.center_y
            ):
                return True

        return False

    def calculate_new_platform_position(self) -> tuple[int, int]:
        highest_platform = self.get_highest_platform()
        next_platform_interval_x = 0
        center_x = highest_platform.platform.bounds.center_x

        while True:
            next_platform_interval_x = BASIC_PLATFORM_SIZE[0] * randint(
                -PLATFORM_SPAWN_DISTANCE_MULTIPLIER,
                PLATFORM_SPAWN_DISTANCE_MULTIPLIER,
            )

            center_x = highest_platform.platform.bounds.center_x + next_platform_interval_x

            if (
                next_platform_interval_x != 0
                and BASIC_PLATFORM_SIZE[0] < center_x
                and center_x < self.screen_w * MINIMAL_SCREEN_DISTANCE - BASIC_PLATFORM_SIZE[0] // 2
            ):
                break
        next_platform_interval_y = self.player_sprite.player.max_jump_height
        center_y = (
            highest_platform.platform.bounds.center_y
            - next_platform_interval_y
            - randint(PLATFORM_Y_MAX_SPAWN_INTERVAL, PLATFORM_Y_MIN_SPAWN_INTERVAL)
        )
        return center_x, center_y

    def spawn_initial_platforms(self) -> None:
        center_x = self.screen_w // 2
        center_y = self.screen_h - FIRST_PLATFORM_SPAWN_Y
        self.spawn_platform(center_x, center_y)
        count_of_platforms = self.screen_h // self.player_sprite.player.max_jump_height * PLATFORMS_COUNT_MULTIPLIER
        for _ in range(count_of_platforms):
            while center_x == 0 or center_y == 0 or self.is_overlapping(center_x, center_y):
                center_x, center_y = self.calculate_new_platform_position()
            self.spawn_platform(center_x, center_y)

    def spawn_new_platform(self) -> None:
        center_x = 0
        center_y = 0
        while center_x == 0 or center_y == 0 or self.is_overlapping(center_x, center_y):
            center_x, center_y = self.calculate_new_platform_position()

        platform_type = PlatformType.BASIC
        platform_moves = random.random() < self.difficulty_params.platform_x_moving_chance

        if platform_moves:
            platform_type = PlatformType.MOBILE
        elif random.random() < self.difficulty_params.onetime_platform_chance:
            platform_type = PlatformType.ONETIME

        self.spawn_platform(center_x, center_y, platform_type)

    def sync_sprite_groups(self) -> None:
        for platform_sprite in self.platforms:
            if not platform_sprite.platform.is_alive:
                self.all_sprites.remove(platform_sprite)
                self.platforms.remove(platform_sprite)
                self.removed_platforms += 1
                self.score += SCORE_INCREASE
            elif platform_sprite not in self.all_sprites:
                self.all_sprites.add(platform_sprite)

    def update(self, delta: float) -> None:
        self.sync_sprite_groups()
        self.delta = delta
        for platform_sprite in self.platforms:
            border = self.platform_spawn_height - self.player_sprite.player.max_jump_height
            border_check = self.player_sprite.rect.centery <= border

            difficulty_check = (
                self.difficulty_params.all_platforms_y_moving_speed
                and self.removed_platforms >= MAX_REMOVED_PLATFORMS_FOR_MOVING_OTHERS
            )

            if border_check or difficulty_check:
                if difficulty_check:
                    offset_y = (
                        (
                            Y_OFFSET_COEFFICIENT * abs(self.player_sprite.rect.centery - self.screen_h)
                            + (ADDITIONAL_Y_OFFSET * self.screen_h)
                        )
                        * delta
                        * self.difficulty_params.all_platforms_y_moving_speed
                    )
                else:
                    offset_y = (
                        (self.platform_spawn_height - self.player_sprite.rect.centery)
                        * delta
                        * PLATFROM_Y_MOVE_MULTIPLIER
                    )

                new_position = (
                    platform_sprite.rect.centerx,
                    platform_sprite.rect.centery + offset_y,
                )

                platform_sprite.set_position(*new_position)

                if self.get_highest_platform().rect.centery > MAX_PLATFORM_HEIGHT:
                    self.spawn_new_platform()

            platform_sprite.platform.velocity.y = 0
