import sys

import pygame
import pygame_gui
from pygame import Surface

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.level_manager import LevelManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.end import EndScreen
from funny_jump.game.screen.intermediate import IntermediateScreen
from funny_jump.game.screen.main_game import MainGameScreen


class GameDirector:
    __slots__ = (
        "asset_manager",
        "caption",
        "clock",
        "end_screen",
        "fps",
        "height",
        "intermediate_screen",
        "is_running",
        "level_manager",
        "main_game_screen",
        "resource_loader",
        "screen",
        "start_screen",
        "ui_manager",
        "vsync",
        "width",
    )

    def __init__(
        self,
        *,
        fps: int,
        width: int,
        height: int,
        caption: str,
        vsync: bool,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
    ) -> None:
        self.asset_manager = asset_manager
        self.resource_loader = resource_loader
        self.fps = fps
        self.width = width
        self.height = height
        self.caption = caption
        self.vsync = vsync
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.level_manager = LevelManager()

    def _init_pygame(self) -> Surface:
        pygame.init()
        pygame.mixer.init()

        screen = pygame.display.set_mode(
            (self.width, self.height),
            vsync=self.vsync,
            flags=pygame.DOUBLEBUF | pygame.SCALED,
        )
        pygame.display.set_caption(self.caption)

        return screen

    def run_game(self) -> None:
        self.screen = self._init_pygame()

        self.ui_manager = pygame_gui.UIManager(
            (self.height, self.width),
            theme_path="src/funny_jump/game/assets/gui_theme.json",
            )

        self.main_game_screen = MainGameScreen(
            resource_loader=self.resource_loader,
            asset_manager=self.asset_manager,
            screen=self.screen,
            width=self.width,
            height=self.height,
            terminate=self.terminate,
            fps=self.fps,
            clock=self.clock,
            level_manager=self.level_manager,
        )

        self.intermediate_screen = IntermediateScreen(
            resource_loader=self.resource_loader,
            asset_manager=self.asset_manager,
            screen=self.screen,
            width=self.width,
            height=self.height,
            terminate=self.terminate,
            fps=self.fps,
            clock=self.clock,
            ui_manager=self.ui_manager,
            level_manager=self.level_manager,
        )

        self.end_screen = EndScreen(
            resource_loader=self.resource_loader,
            asset_manager=self.asset_manager,
            screen=self.screen,
            width=self.width,
            height=self.height,
            terminate=self.terminate,
            fps=self.fps,
            clock=self.clock,
        )

        self.is_running = True
        self._run_main_loop()

    def terminate(self) -> None:
        self.is_running = False
        pygame.quit()
        sys.exit()

    def _run_main_loop(self) -> None:
        if not self.screen:
            raise RuntimeError("Invoke run_game() first.")

        while True:
            self.intermediate_screen.run()
            self.main_game_screen.run()
