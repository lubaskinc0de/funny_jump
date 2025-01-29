import pygame.sprite

from funny_jump.game.sprites.player import PlayerSprite


class PlatformManager:
    def __init__(
        self,
        platforms: pygame.sprite.Group,  # type: ignore
        screen_w: int,
        screen_h: int,
        player_sprite: PlayerSprite,
    ) -> None:
        self.player_sprite = player_sprite
        self.platforms = platforms
        self.screen_w = screen_w
        self.screen_h = screen_h

    def update(self) -> None: ...
