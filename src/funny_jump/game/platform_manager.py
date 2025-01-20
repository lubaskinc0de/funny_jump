import pygame.sprite

from funny_jump.domain.value_object.velocity import Velocity
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.game.sprites.player import PlayerSprite
from funny_jump.game.sprites.platform import PlatformSprite
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite
from funny_jump.domain.entity.platform import BasicPlatform
from random import randint
from funny_jump.game.path_to_assets import Asset
from funny_jump.engine.asset_manager import AssetManager

BASIC_PLATFORM_SIZE = (200, 60)


class PlatformManager:
    def __init__(
        self,
        platforms: pygame.sprite.Group,  # type: ignore  # noqa: PGH003
        screen_w: int,
        screen_h: int,
        player_sprite: PlayerSprite,
        asset_manager: AssetManager
    ) -> None:
        self.player_sprite = player_sprite
        self.platforms = platforms
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.asset_manager = asset_manager
                
    def rand_platforms(self): 
        ...

    def spawn_platform(self, center_x: int, center_y: int) -> None:
        platform = BasicPlatform(
            screen_h=self.screen_h,
            velocity=Velocity(),
            bounds=Bounds(center_x, center_y),
        )
        
        platform_sprite = BasicPlatformSprite(
            platform=platform,
            image=self.asset_manager.get_asset_path(Asset.PLATFORM_SPRITE),
            size=BASIC_PLATFORM_SIZE
        )
        platform_sprite.set_position(center_x, center_y)
        self.platforms.add(platform_sprite)

    def spawn_platforms(self) -> None:
        if len(self.platforms) == 0:
            center_y = self.screen_h - 1000 # Временно
            # count_platoforms = self.rand_platforms()
            for y in range(self.screen_h // BASIC_PLATFORM_SIZE[1]):
                # count_of_x_platforms = randint(self.screen_w // BASIC_PLATFORM_SIZE[0])
                minimum_spawn_distance = 20 + BASIC_PLATFORM_SIZE[0] // 2
                for _ in range(self.screen_w // BASIC_PLATFORM_SIZE[1]):
                    self.spawn_platform(minimum_spawn_distance, center_y)
                    minimum_spawn_distance *= minimum_spawn_distance  # !!!!!!! ДОРАБОТАТЬ!
                    # minimum_spawn_distance += randint(minimum_spawn_distance, self.screen_w - 50)
                    if minimum_spawn_distance > self.screen_w:
                        break
                
            # center_x = 350 # |
            # for n in range(5): # |  Временный тест код (потом будет заменен на генерацию)
            #     center_y = 1000 / 5 * n # |
            #     center_x += n * 30 # |
            #     platform = BasicPlatform(
            #         screen_h=self.screen_h,
            #         velocity=Velocity(),
            #         bounds=Bounds(center_x, center_y),
            #     )
                
            #     platform_sprite = BasicPlatformSprite(
            #         platform=platform,
            #         image=self.asset_manager.get_asset_path(Asset.PLATFORM_SPRITE),
            #         size=BASIC_PLATFORM_SIZE
            #     )
            #     platform_sprite.set_position(center_x, center_y)
            #     self.platforms.add(platform_sprite)

    def update(self) -> None:
        self.spawn_platforms()
        
        if self.player_sprite.rect.centery <= self.screen_h // 2:
            for platform_sprite in self.platforms:
                platform_sprite: BasicPlatformSprite
                platform_sprite.move_down()
