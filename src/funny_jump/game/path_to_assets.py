from enum import Enum, auto
from pathlib import Path


class Asset(Enum):
    BG_MUSIC = auto()
    BG_IMG = auto()
    PLAYER_STATIC_SPRITE = auto()
    PLATFORM_SPRITE = auto()


ASSET_PATH = {
    Asset.BG_MUSIC: Path("sounds/soundtrack.mp3"),
    Asset.BG_IMG: Path("bg.jpg"),
    Asset.PLATFORM_SPRITE: Path("sprites/platform.png"),
    Asset.PLAYER_STATIC_SPRITE: Path("sprites/frog/idle/00.png"),
}
