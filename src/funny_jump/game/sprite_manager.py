from typing import Any

import pygame
from pygame import Surface

from funny_jump.domain.entity.player import Player
from funny_jump.engine.animation.animation_loader import IncrementalAnimationLoader
from funny_jump.engine.animation.animation_manager import Animation, AnimationId, AnimationManagerDummy
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.collision_manager import CollisionManager
from funny_jump.game.level_manager import LevelManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.platform_manager import BASIC_PLATFORM_SIZE, PlatformManager
from funny_jump.game.sprites.player import HOP_ANIMATION_ID, PlayerSounds, PlayerSprite


class SpriteManager:
    __slots__ = (
        "all_sprites",
        "asset_manager",
        "collision_manager",
        "height",
        "level_manager",
        "platform_manager",
        "platforms",
        "player",
        "player",
        "player_sprite",
        "resource_loader",
        "screen",
        "width",
    )

    def __init__(
        self,
        screen: Surface,
        width: int,
        height: int,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
        level_manager: LevelManager,
        player: Player,
    ) -> None:
        self.resource_loader = resource_loader
        self.asset_manager = asset_manager
        self.screen = screen
        self.width = width
        self.height = height
        self.level_manager = level_manager
        self.player = player

        sound_loader = pygame.mixer.Sound
        player_jump_sound = self.asset_manager.get_asset(Asset.PLAYER_JUMP_SOUND, sound_loader)
        player_jump_sound.set_volume(0.2)

        player_sounds = PlayerSounds(
            jump=player_jump_sound,
        )
        player_hop_anim_loader = IncrementalAnimationLoader(
            self.asset_manager.get_asset_path(Asset.PLAYER_JUMP_FRAMES),
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
            (54, 54),
            animation_manager=player_animation_manager,
            sounds=player_sounds,
        )

        player_pos = self.width // 2, self.height - 200 - BASIC_PLATFORM_SIZE[1] * 1.6
        self.player_sprite.set_position(*player_pos)

        self.all_sprites: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.all_sprites.add(self.player_sprite)

        self.platforms: pygame.sprite.Group[Any] = pygame.sprite.Group()

        self.collision_manager = CollisionManager(
            self.player_sprite,
            self.platforms,
            self.player,
        )

        current_level = self.level_manager.get_current_level()

        self.platform_manager = PlatformManager(
            self.all_sprites,
            self.platforms,
            self.width,
            self.height,
            self.player_sprite,
            self.asset_manager,
            current_level.difficulty_parameters,
        )

    @property
    def player_score(self) -> int:
        return self.platform_manager.score

    def update(self, delta: float) -> None:
        self.platform_manager.update(delta=delta)
        self.all_sprites.update(delta)
        self.collision_manager.check_collisions()

    def draw(self) -> None:
        self.all_sprites.draw(self.screen)
