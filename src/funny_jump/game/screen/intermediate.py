from collections.abc import Callable

import pygame
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.base import BaseScreen
from funny_jump.game.text_manager import TextManager


class IntermediateScreen(BaseScreen):
    __slots__ = (
        "asset_manager",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "logo_font_size",
        "resource_loader",
        "score",
        "screen",
        "terminate",
        "text_coord",
        "text_font_size",
        "text_render_manager",
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
        self.score = score

    def render_all(self) -> None:
        logo_text = "Поздравляем!"
        logo_font = pygame.font.Font(None, self.width // 6)
        logo_font.bold = True

        score_text = f"Уровень пройден! Ваш результат - {self.score} очков"

        text_font = pygame.font.Font(None, self.width // 11)

        offer_text = "Пора начать следующий уровень!"
        mouse_text = "Нажмите на любую клавишу мыши, чтобы продолжить"

        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
        )

        text_render_manager.render_as_logo(logo_text)
        text_render_manager.render_as_text(score_text)
        text_render_manager.render_as_text(offer_text)
        text_render_manager.render_as_text(mouse_text)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame.MOUSEBUTTONDOWN:
                    self.is_running = False
