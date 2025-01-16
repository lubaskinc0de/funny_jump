
import pygame.sprite

from funny_jump.game.sprites.player import PlayerSprite
from funny_jump.game.sprites.platform import PlatformSprite
from funny_jump.game.sprites.basic_platform import BasicPlatform
from random import randint


class PlatformManager:
    def __init__(
        self,
        platforms: pygame.sprite.Group[PlatformSprite],  # type: ignore  # noqa: PGH003
        screen_w: int,
        screen_h: int,
        player_sprite: PlayerSprite,
    ) -> None:
        self.player_sprite = player_sprite
        self.platforms = platforms
        self.screen_w = screen_w
        self.screen_h = screen_h

    def rand_platforms(): ...

    def spawn_platforms() -> None:
        ... 

    def update(self) -> None:
        # self.player_sprite = PlayerSprite(
        #     self.player,
        #     self.asseat_manager.get_asset_path(Asset.PLAYER_STATIC_SPRITE),
        #     (64, 64),
        # )
        screen_middle = self.screen_h // 2
        if self.player_sprite.player.center_y >= screen_middle:
            free_space = screen_middle - self.player_sprite.player.center_y
            for platform_sprite in self.platforms:
                platform_sprite: BasicPlatform
                platform_sprite.update()
                platform_sprite.move_down()
                
