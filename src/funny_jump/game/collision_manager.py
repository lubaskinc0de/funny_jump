from dataclasses import dataclass

import pygame

from funny_jump.domain.entity.player import Player
from funny_jump.domain.service.platform_collide import on_player_collide_platform
from funny_jump.engine.collider import collider_top
from funny_jump.game.sprites.platform_sprite import PlatformSprite
from funny_jump.game.sprites.player import PlayerSprite


@dataclass(slots=True, frozen=True)
class CollisionManager:
    player_sprite: PlayerSprite
    platforms: pygame.sprite.Group  # type: ignore
    player: Player

    def check_collisions(self) -> None:
        self._check_player_collides_platforms()

    def _check_player_collides_platforms(self) -> None:
        player_rect = self.player_sprite.rect
        collide: list[PlatformSprite] = pygame.sprite.spritecollide(
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
            if self.player.staying_at is not None and any(
                self.player.staying_at.bounds == collided.platform.bounds for collided in collide
            ):
                return
            self.player.left_from_ground()
            return

        for platform_sprite in collide:
            platform_rect = platform_sprite.rect

            if collider_top(platform_rect, self.player_sprite.prev_pos, player_rect):
                self.player_sprite.set_position(
                    player_rect.centerx,
                    (platform_rect.top - player_rect.height // 2) + 2,
                )
                on_player_collide_platform(platform_sprite.platform, self.player)
                return
