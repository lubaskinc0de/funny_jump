from collections.abc import Callable
from functools import partial
from pathlib import Path

import pygame
from pygame import Surface
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset


def get_bg(width: int, height: int, path: Path) -> Surface:
    bg = pygame.image.load(path)
    bg = pygame.transform.scale(bg, (width, height))
    return bg


class StartScreen:
    __slots__ = (
        "asset_manager",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "resource_loader",
        "screen",
        "terminate",
        "width",
    )

    def __init__(
        self,
        *,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
        screen: pygame.Surface,
        width: int,
        height: int,
        terminate: Callable[[], None],
        fps: int,
        clock: pygame.time.Clock,
    ) -> None:
        self.resource_loader = resource_loader
        self.asset_manager = asset_manager
        self.is_running = False
        self.screen = screen
        self.width = width
        self.height = height
        self.get_bg: Callable[[Path], Surface] = partial(get_bg, self.width, self.height)
        self.terminate = terminate
        self.clock = clock
        self.fps = fps

    def run(self) -> None:
        self.is_running = True
        self._run_main_loop()

    def _run_main_loop(self) -> None:
        while self.is_running:
            self._dispatch_events(pygame.event.get())

            bg_img = self.asset_manager.get_asset(Asset.GAME_BG_IMG, self.get_bg)
            self.screen.blit(bg_img, (0, 0))

            pygame.display.flip()
            self.clock.tick(self.fps)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame.MOUSEBUTTONDOWN:
                    self.is_running = False
