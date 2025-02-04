from collections.abc import Callable
from functools import partial
from pathlib import Path

import pygame
import pygame_gui
from pygame import Surface
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset


def get_bg(width: int, height: int, path: Path) -> Surface:
    bg = pygame.image.load(path)
    bg = pygame.transform.scale(bg, (width, height))
    return bg


class BaseScreen:
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
        self.load_bg()
        self.render_all()
        while self.is_running:
            self._dispatch_events(pygame.event.get())
            pygame.display.flip()
            self.clock.tick(self.fps)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()

    def load_bg(self) -> None:
        bg_img = self.asset_manager.get_asset(Asset.GAME_BG_IMG, self.get_bg)
        self.screen.blit(bg_img, (0, 0))

    def render_all(self) -> None: ...


class ButtonScreen(BaseScreen):
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
        "ui_manager",
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
        ui_manager: pygame_gui.UIManager,
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
        self.ui_manager = ui_manager

    def _run_main_loop(self) -> None:
        self.load_bg()
        self.render_all()
        while self.is_running:
            self._dispatch_events(pygame.event.get())
            pygame.display.flip()
            delta = self.clock.tick(self.fps) / 1000

            self.ui_manager.update(delta)
            self.ui_manager.draw_ui(self.screen)
