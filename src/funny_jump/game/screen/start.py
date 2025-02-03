from collections.abc import Callable

import pygame
import pygame_gui
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.button import Button
from funny_jump.game.button_manager import ButtonManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.base import ButtonScreen
from funny_jump.game.text_manager import TextManager


class StartScreen(ButtonScreen):
    __slots__ = (
        "asset_manager",
        "clock",
        "fps",
        "game_run_button_name",
        "get_bg",
        "height",
        "is_running",
        "menu_buttons",
        "quit_button_name",
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
            ui_manager=ui_manager,
        )
        self.game_run_button_name = "game_run_button"
        self.quit_button_name = "quit_button"
        self.menu_buttons: dict[pygame_gui.elements.UIButton, str]

    def render_all(self) -> None:
        buttons = [
            Button(self.game_run_button_name, "Начать игру"),
            Button(self.quit_button_name, "Выйти из игры"),
        ]

        button_manager = ButtonManager(
            width=self.width,
            height=self.height,
            ui_manager=self.ui_manager,
        )

        self.menu_buttons = button_manager.create_button_menu(buttons=buttons)

        logo_font = pygame.font.Font(None, int(self.width // 5.5))
        logo_font.bold = True

        text_font = pygame.font.Font(None, self.width // 11)

        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
        )

        logo_text = "FUNNY JUMP"

        text_render_manager.render_as_logo(logo_text)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame_gui.UI_BUTTON_PRESSED:
                    if self.menu_buttons[event.ui_element] == self.game_run_button_name:
                        self.is_running = False
                        # Библиотека содержит неаннотированную функцию, на что ругается mypy
                        self.ui_manager.clear_and_reset() # type: ignore
                    elif self.menu_buttons[event.ui_element] == self.quit_button_name:
                        self.is_running = False
                        self.terminate()
            self.ui_manager.process_events(event)
