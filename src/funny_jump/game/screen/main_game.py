from collections.abc import Callable
from functools import partial
from pathlib import Path

import pygame
from pygame import Surface
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.sprite_manager import SpriteManager


def get_bg(width: int, height: int, path: Path) -> Surface:
    bg = pygame.image.load(path)
    bg = pygame.transform.scale(bg, (width, height))
    return bg


class MainGameScreen:
    __slots__ = (
        "asset_manager",
        "assets",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "resource_loader",
        "screen",
        "sprite_manager",
        "terminate",
        "width",
    )

    def __init__(
        self,
        *,
        fps: int,
        width: int,
        height: int,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        terminate: Callable[[], None],
    ) -> None:
        self.clock = clock
        self.screen = screen
        self.fps = fps
        self.width = width
        self.height = height
        self.resource_loader = resource_loader
        self.asset_manager = asset_manager
        self.sprite_manager = SpriteManager(
            screen=self.screen,
            width=self.width,
            height=self.height,
            resource_loader=self.resource_loader,
            asset_manager=asset_manager,
        )
        self.is_running = False
        self.terminate = terminate
        self.get_bg: Callable[[Path], Surface] = partial(get_bg, self.width, self.height)

    def run(self) -> None:
        self.is_running = True
        self._run_main_loop()

    def _run_main_loop(self) -> None:
        pygame.mixer.music.load(self.asset_manager.get_asset_path(Asset.GAME_BG_MUSIC))
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        pygame.mixer.music.set_volume(0.2)

        delta = 0.0
        while self.is_running:
            self._dispatch_events(pygame.event.get())
            self.sprite_manager.update(delta)

            bg_img = self.asset_manager.get_asset(Asset.GAME_BG_IMG, self.get_bg)
            self.screen.blit(bg_img, (0, 0))

            self.sprite_manager.draw()

            pygame.display.flip()
            delta = self.clock.tick(self.fps) / 1000

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
