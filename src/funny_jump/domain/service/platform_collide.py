from funny_jump.domain.entity.platforms import Platform
from funny_jump.domain.entity.player import Player


def on_player_collide_platform(platform: Platform, player: Player) -> None:
    player.get_on_ground(platform)
    platform.on_collide()
