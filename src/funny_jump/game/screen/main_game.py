from collections.abc import Callable

import pygame
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.base import BaseScreen
from funny_jump.game.sprite_manager import SpriteManager


class MainGameScreen(BaseScreen):
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
        super().__init__(
            resource_loader=resource_loader,
            asset_manager=asset_manager,
            screen=screen,
            width=width,
            height=height,
            terminate=terminate,
            fps=fps,
            clock=clock,
        )
        self.sprite_manager = SpriteManager(
            screen=self.screen,
            width=self.width,
            height=self.height,
            resource_loader=self.resource_loader,
            asset_manager=asset_manager,
        )
        self.is_running = False

    def _run_main_loop(self) -> None:
        pygame.mixer.music.load(self.asset_manager.get_asset_path(Asset.GAME_BG_MUSIC))
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        pygame.mixer.music.set_volume(0.2)

        delta = 0.0
        while self.is_running:
            self._dispatch_events(pygame.event.get())
            self.sprite_manager.update(delta)

            self.load_bg()

            self.sprite_manager.draw()

            pygame.display.flip()
            delta = self.clock.tick(self.fps) / 1000

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
