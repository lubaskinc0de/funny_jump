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
        self.spawn_interval = 0.05
        self.platform_spawn_heigth = self.screen_h // 2 - 150
        
        self.spawn_initial_platforms()
        
        
    def rand_platforms(self): 
        ...

    def spawn_platform(self, center_x: int, center_y: int) -> None:
        platform = BasicPlatform(
            screen_h=self.screen_h,
            velocity=Velocity(),
            bounds=Bounds(center_x, center_y),
        )
        print(platform.bounds.center_y)
        
        platform_sprite = BasicPlatformSprite(
            platform=platform,
            image=self.asset_manager.get_asset_path(Asset.PLATFORM_SPRITE),
            size=BASIC_PLATFORM_SIZE
        )
        platform_sprite.set_position(center_x, center_y)
        print(center_y)
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
    
    def spawn_initial_platforms(self) -> None:
        center_y = self.screen_h - 100
        for _ in range(30):
            center_x = randint(50, self.screen_w - 50)
            if not self.is_overlapping(center_x, center_y):
                self.spawn_platform(center_x, center_y)
                center_y -= randint(40, 50)
    
    def spawn_new_platforms(self, delta: float) -> None:
        self.last_spawn_time += delta
        if self.player_sprite.rect.centery <= self.screen_h // 2: #and self.last_spawn_time >= self.spawn_interval:
                
            self.last_spawn_time = 0

            number_of_platforms_to_spawn = 5

            for _ in range(number_of_platforms_to_spawn):
                center_x = randint(50, self.screen_w - 50)
                # center_y = randint(100, 200)
                center_y = -randint(50, 100)
                if len(self.platforms) <= 36:
                    if center_y <= self.player_sprite.player.max_jump_height + 200:
                        if not self.is_overlapping(center_x, center_y):
                            self.spawn_platform(center_x, center_y)

    def update(self, delta: float) -> None:
        self.spawn_new_platforms(delta)
        if self.player_sprite.rect.centery <= self.screen_h // 2:
            for platform_sprite in self.platforms:
                platform_sprite: BasicPlatformSprite
                speed_mult = (self.screen_h - self.player_sprite.rect.centery) * delta  * 0.1
                platform_sprite.move_down(speed_mult)
                print(speed_mult)
        else:
            for platform_sprite in self.platforms:
                platform_sprite.platform.velocity.y = 0
                
