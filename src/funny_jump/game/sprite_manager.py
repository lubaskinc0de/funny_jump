import pygame
from pygame import Surface

from funny_jump.domain.entity.player import Player
from funny_jump.domain.service.platform_collide import on_player_collide_platform
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.sprites.basic_platform import BasicPlatformSprite
from funny_jump.game.sprites.player import PlayerSprite


class SpriteManager:
    __slots__ = (
        "all_sprites",
        "asset_manager",
        "height",
        "platforms",
        "player",
        "player_sprite",
        "resource_loader",
        "screen",
        "width",
    )

    def __init__(
        self,
        player: Player,
        screen: Surface,
        width: int,
        height: int,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
    ) -> None:
        self.player = player
        self.screen = screen
        self.width = width
        self.height = height
        self.resource_loader = resource_loader
        self.asset_manager = asset_manager

        self.player_sprite = PlayerSprite(
            self.player,
            self.asset_manager.get_asset_path(Asset.PLAYER_STATIC_SPRITE),
            (64, 64),
        )
        player_pos = self.width // 2, self.height - self.height // 10
        self.player_sprite.set_position(*player_pos)

        # https://github.com/pygame/pygame/issues/4392
        self.all_sprites = pygame.sprite.Group()  # type: ignore  # noqa: PGH003
        self.platforms = pygame.sprite.Group()  # type: ignore  # noqa: PGH003

        self.all_sprites.add(self.player_sprite)

    def _check_collisions(self) -> None:
        self._check_player_collides_platforms()

    def _check_player_collides_platforms(self) -> None:
        player_rect = self.player_sprite.rect
        collide: list[BasicPlatformSprite] = pygame.sprite.spritecollide(
            self.player_sprite,
            self.platforms,
            dokill=False,
        )

        if not collide and self.player.on_ground:
            self.player.left_from_ground()
            return

        if not collide:
            return

        if self.player.on_ground:
            return

        for platform_sprite in collide:
            platform_rect = platform_sprite.rect
            prev_bottom = player_rect.bottom - self.player.velocity_y

            if (prev_bottom <= platform_rect.top) and (platform_rect.top < player_rect.bottom):
                self.player_sprite.set_position(
                    player_rect.centerx,
                    (platform_rect.top - player_rect.height // 2) + 2,
                )
                on_player_collide_platform(platform_sprite.platform, self.player)
                return

    def update(self) -> None:
        self._check_collisions()
        self.all_sprites.update()

    def draw(self) -> None:
        self.all_sprites.draw(self.screen)
