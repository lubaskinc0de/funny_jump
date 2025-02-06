import logging
import sys

import pygame
import pygame_gui
from pygame import Surface

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.exception.base import BaseError
from funny_jump.game.level_manager import LevelManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.score.score_storage import ScoreStorage
from funny_jump.game.screen.end import EndScreen
from funny_jump.game.screen.level_choice import LevelChoiceScreen
from funny_jump.game.screen.main_game import MainGameScreen


class GameDirector:
    __slots__ = (
        "asset_manager",
        "caption",
        "clock",
        "end_screen",
        "fps",
        "height",
        "is_running",
        "level_choice_screen",
        "level_manager",
        "main_game_screen",
        "resource_loader",
        "score_storage",
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
        score_storage: ScoreStorage,
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
        self.score_storage = score_storage

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
            (self.width, self.height),
            theme_path=self.asset_manager.get_asset_path(Asset.GUI_TEMPLATE),
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
            score_storage=self.score_storage,
        )

        self.level_choice_screen = LevelChoiceScreen(
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
            try:
                self.level_choice_screen.run()
                self.main_game_screen.run()
                level = self.level_manager.get_current_level()
                self.end_screen.score = self.main_game_screen.score
                self.end_screen.best_score = self.score_storage.get_best_score(level)
            except BaseError as exc:
                self.end_screen.error_text = exc.MESSAGE
            else:
                self.end_screen.error_text = None

            try:
                self.end_screen.run()
            except BaseError:
                logging.exception("While running end screen:")
                self.terminate()
