from collections.abc import Callable

import pygame
import pygame_gui
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.button import Button
from funny_jump.game.button_manager import ButtonManager
from funny_jump.game.level_manager import LevelManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.base import ButtonScreen
from funny_jump.game.text_manager import TextManager

SCREEN_WIDTH_FONT_SIZE_DIVISOR = 11
SCREEN_WIDTH_LOGO_FONT_SIZE_DIVISOR = 6


class LevelChoiceScreen(ButtonScreen):
    __slots__ = (
        "asset_manager",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "level_buttons",
        "level_manager",
        "resource_loader",
        "score",
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
        score: int = 0,
        ui_manager: pygame_gui.UIManager,
        level_manager: LevelManager,
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
            ui_manager=ui_manager,
        )
        self.score = score
        self.level_manager = level_manager

        buttons = [
            Button(str(level_id), f"Уровень {level.name}") for level_id, level in enumerate(self.level_manager.levels)
        ]

        button_manager = ButtonManager(
            width=self.width,
            height=self.height,
            ui_manager=self.ui_manager,
        )

        self.level_buttons = button_manager.create_button_menu(
            buttons=buttons,
            size=1.5,
        )

    def render_all(self) -> None:
        logo_text = "Выбор уровня"
        logo_font = pygame.font.Font(
            None, 
            self.width // SCREEN_WIDTH_LOGO_FONT_SIZE_DIVISOR
            )
        logo_font.bold = True

        text_font = pygame.font.Font(
            None, 
            self.width // SCREEN_WIDTH_FONT_SIZE_DIVISOR
            )

        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
        )

        text_render_manager.render_as_logo(logo_text)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame_gui.UI_BUTTON_PRESSED:
                    self.render_all()
                    self.level_manager.change_level(int(self.level_buttons[event.ui_element]))
                    self.is_running = False
            self.ui_manager.process_events(event)
