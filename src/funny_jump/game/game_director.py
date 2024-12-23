from collections.abc import Callable
from functools import partial
from pathlib import Path

import pygame
from pygame import Surface
from pygame.event import Event

from funny_jump.domain.entity.player import Player
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.sprite_manager import SpriteManager


def get_bg(width: int, height: int, path: Path) -> Surface:
    bg = pygame.image.load(path)
    bg = pygame.transform.scale(bg, (width, height))
    return bg


class GameDirector:
    __slots__ = (
        "asset_manager",
        "assets",
        "caption",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "player",
        "resource_loader",
        "screen",
        "sprite_manager",
        "vsync",
        "width",
    )

    def __init__(
        self,
        *,
        fps: int,
        width: int,
        height: int,
        player: "Player",
        caption: str,
        vsync: bool,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
    ) -> None:
        self.fps = fps
        self.width = width
        self.height = height
        self.player = player
        self.caption = caption
        self.vsync = vsync
        self.resource_loader = resource_loader
        self.asset_manager = asset_manager

        self.screen = self._init_pygame()
        self.clock = pygame.time.Clock()
        self.sprite_manager = SpriteManager(
            player=self.player,
            screen=self.screen,
            width=self.width,
            height=self.height,
            resource_loader=self.resource_loader,
            asset_manager=asset_manager,
        )
        self.is_running = False

        self.get_bg: Callable[[Path], Surface] = partial(get_bg, self.width, self.height)

    def _init_pygame(self) -> Surface:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.asset_manager.get_asset_path(Asset.BG_MUSIC))
        pygame.mixer.music.play(loops=-1, fade_ms=500)

        screen = pygame.display.set_mode(
            (self.width, self.height),
            vsync=self.vsync,
            flags=pygame.DOUBLEBUF | pygame.SCALED,
        )
        pygame.display.set_caption(self.caption)

        return screen

    def run_game(self) -> None:
        self.is_running = True
        self._run_main_loop()

    def _run_main_loop(self) -> None:
        if not self.screen:
            raise RuntimeError("Invoke run_game() first.")

        while self.is_running:
            self._dispatch_events(pygame.event.get())
            self.sprite_manager.update()

            bg_img = self.asset_manager.get_asset(Asset.BG_IMG, self.get_bg)
            self.screen.blit(bg_img, (0, 0))

            self.sprite_manager.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
