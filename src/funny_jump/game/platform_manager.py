import pygame.sprite

from funny_jump.domain.value_object.velocity import Velocity
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.game.sprites.player import PlayerSprite
from funny_jump.game.sprites.platform import PlatformSprite
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite
from funny_jump.domain.entity.platform import BasicPlatform
from random import randint, randrange
from funny_jump.game.path_to_assets import Asset
from funny_jump.engine.asset_manager import AssetManager

BASIC_PLATFORM_SIZE = (100, 30)


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
        self.last_spawn_time = 0
        self.spawn_interval = 0.2
        self.platform_spawn_height = self.screen_h // 2
        self.last_center_y: int = 0
        self.spawn_initial_platforms()

    def get_highest_platform(self) -> BasicPlatformSprite:
        highest_platform_sprite: BasicPlatformSprite = None
        for platform_sprite in self.platforms:
            if not highest_platform_sprite:
                highest_platform_sprite = platform_sprite
                continue
            platform_sprite: BasicPlatformSprite
            if platform_sprite.platform.bounds.center_y < highest_platform_sprite.platform.bounds.center_y:
                highest_platform_sprite = platform_sprite
        return highest_platform_sprite
    
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
        
    def is_overlapping(self, center_x: int, center_y: int) -> bool:
        new_bounds = Bounds(center_x, center_y)

        for platform_sprite in self.platforms:
            existing_bounds = platform_sprite.platform.bounds
            
            if (
                new_bounds.center_x < existing_bounds.center_x + existing_bounds.width + randint(50, 200) and
                new_bounds.center_x + BASIC_PLATFORM_SIZE[0] > existing_bounds.center_x and
                new_bounds.center_y < existing_bounds.center_y + existing_bounds.height + randint(30, 70) and
                new_bounds.center_y + BASIC_PLATFORM_SIZE[1] > existing_bounds.center_y
                ):
                return True

        return False
    
    def calculate_new_platform_position(self) -> tuple[int, int]:
        highest_platform = self.get_highest_platform()
        next_platform_interval_x = 0
        center_x = highest_platform.platform.bounds.center_x
        while True:
            next_platform_interval_x = BASIC_PLATFORM_SIZE[0] * randint(-3, 3)
            center_x = highest_platform.platform.bounds.center_x + next_platform_interval_x
            if next_platform_interval_x != 0:
                if BASIC_PLATFORM_SIZE[0] < center_x:
                    if center_x < self.screen_w - BASIC_PLATFORM_SIZE[0] // 2:
                        break
            
        next_platform_interval_y = self.player_sprite.player.max_jump_height // randint(1, 2)
        center_y = highest_platform.platform.bounds.center_y - next_platform_interval_y
        # print("----->", highest_platform.rect.centery)
        # print(center_x, center_y)
        print("----->", abs(center_y - highest_platform.rect.centery))
        if abs(center_y - highest_platform.rect.centery) > self.player_sprite.player.max_jump_height: exit()
        else: print(self.player_sprite.player.max_jump_height)
        print()
        return center_x, center_y

    def spawn_initial_platforms(self) -> None:
        # center_y = self.screen_h - 100
        
        #     center_x = randint(50, self.screen_w - 50)
        #     if not self.is_overlapping(center_x, center_y):
        #         self.spawn_platform(center_x, center_y)
        #         center_y -= self.player_sprite.player.max_jump_height + randint(0, 50)
        center_x = self.screen_w // 2
        center_y = self.screen_h - 200
        self.spawn_platform(center_x, center_y)
        for _ in range(7):
            while center_x == 0 or center_y == 0 or self.is_overlapping(center_x, center_y):
                center_x, center_y = self.calculate_new_platform_position()
            self.spawn_platform(center_x, center_y)
    
    def spawn_new_platforms(self) -> None:
        center_x = 0
        center_y = 0
        while center_x == 0 or center_y == 0 or self.is_overlapping(center_x, center_y):
            center_x, center_y = self.calculate_new_platform_position()
        
        self.spawn_platform(center_x, center_y)

    def update(self, delta: float) -> None:
        if self.player_sprite.rect.centery <= self.platform_spawn_height:
            for platform_sprite in self.platforms:
                platform_sprite: BasicPlatformSprite
                speed_mult = (self.screen_h - self.player_sprite.rect.centery) * delta  * 0.15
                if self.player_sprite.player.velocity.y < 0:
                    platform_sprite.move_down(speed_mult)
            if self.get_highest_platform().rect.centery > -5000:
                self.spawn_new_platforms()
            # if self.get_highest_platform().platform.bounds.center_y < -4700:
            #     for platform_sprite in self.platforms:
            #         platform_sprite: BasicPlatformSprite
            #         from pprint import pprint
            #         pprint(platform_sprite.rect.centerx)
            #         pprint(platform_sprite.rect.centery)
            #         print("_____________")
            #     exit()
        else:
            for platform_sprite in self.platforms:
                platform_sprite.platform.velocity.y = 0
                
