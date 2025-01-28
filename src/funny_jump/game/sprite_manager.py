from typing import Any

import pygame
from pygame import Surface

from funny_jump.domain.entity.player import Player
from funny_jump.engine.animation.animation_loader import IncrementalAnimationLoader
from funny_jump.engine.animation.animation_manager import Animation, AnimationId, AnimationManagerDummy
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.collision_manager import CollisionManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.platform_manager import PlatformManager
from funny_jump.game.sprites.player import HOP_ANIMATION_ID, PlayerSprite


class SpriteManager:
    __slots__ = (
        "all_sprites",
        "asset_manager",
        "collision_manager",
        "height",
        "platform_manager",
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

        player_hop_anim_loader = IncrementalAnimationLoader(
            self.asset_manager.get_asset_path(Asset.PLAYER_HOP),
        )
        player_hop_anim = Animation(
            animation_id=AnimationId(HOP_ANIMATION_ID),
            duration=1,
            frames=player_hop_anim_loader.load_frames(),
        )
        player_animation_manager = AnimationManagerDummy(
            animations={
                HOP_ANIMATION_ID: player_hop_anim,
            },
        )

        self.player_sprite = PlayerSprite(
            self.player,
            self.asset_manager.get_asset_path(Asset.PLAYER_STATIC_SPRITE),
            (64, 64),
            animation_manager=player_animation_manager,
        )

        player_pos = self.width // 2, self.height - self.height // 10
        self.player_sprite.set_position(*player_pos)

        self.all_sprites: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.platforms: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.all_sprites.add(self.player_sprite)
        self.collision_manager = CollisionManager(
            self.player_sprite,
            self.platforms,
            self.player,
            self.screen,
        )
        self.platform_manager = PlatformManager(
            self.platforms,
            self.width,
            self.height,
            self.player_sprite,
            self.asset_manager,
        )

    def update(self, delta: float) -> None:
        self.collision_manager.check_collisions()
        self.platform_manager.update()
        for platform_sprite in self.platforms:
            if not platform_sprite.platform.is_alive:
                self.all_sprites.remove(platform_sprite)
                self.platforms.remove(platform_sprite)
            elif platform_sprite not in self.all_sprites:
                self.all_sprites.add(platform_sprite)
        self.all_sprites.update(delta)

    def draw(self) -> None:
        self.all_sprites.draw(self.screen)
