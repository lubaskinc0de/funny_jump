from enum import Enum, auto
from pathlib import Path


class Asset(Enum):
    GAME_BG_MUSIC = auto()
    GAME_BG_IMG = auto()
    PLAYER_STATIC_SPRITE = auto()
    PLATFORM_SPRITE = auto()
    MOBILE_PLATFORM_SPRITE = auto()
    PLAYER_JUMP_FRAMES = auto()
    PLAYER_JUMP_SOUND = auto()
    GUI_TEMPLATE = auto()
    ONETIME_PLATFORM = auto()
    ONETIME_PLATFORM_RED = auto()


ASSET_PATH = {
    Asset.GAME_BG_MUSIC: Path("sounds/soundtrack.mp3"),
    Asset.GAME_BG_IMG: Path("bg.jpg"),
    Asset.PLATFORM_SPRITE: Path("sprites/platform.png"),
    Asset.MOBILE_PLATFORM_SPRITE: Path("sprites/mobile_platform.png"),
    Asset.PLAYER_STATIC_SPRITE: Path("sprites/frog/idle/00.png"),
    Asset.PLAYER_JUMP_FRAMES: Path("sprites/frog/hop/"),
    Asset.PLAYER_JUMP_SOUND: Path("sounds/jump.wav"),
    Asset.GUI_TEMPLATE: Path("gui_theme.json"),
    Asset.ONETIME_PLATFORM: Path("sprites/onetime_platform.png"),
    Asset.ONETIME_PLATFORM_RED: Path("sprites/onetime_platform_red.png"),
}
