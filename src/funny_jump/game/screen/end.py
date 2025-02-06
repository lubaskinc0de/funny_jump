from collections.abc import Callable

import pygame
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.font import get_font_size
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.base import BaseScreen
from funny_jump.game.text_manager import TextManager

MID_RESULT = 50
HIGH_RESULT = 200


class EndScreen(BaseScreen):
    __slots__ = (
        "asset_manager",
        "best_score",
        "clock",
        "error_text",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "resource_loader",
        "score",
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
        error_text: str | None = None,
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
        self.score = 0
        self.error_text = error_text
        self.best_score = 0

    def render_all(self) -> None:
        logo_text = "КОНЕЦ"
        logo_font_size = get_font_size(self.width, self.height, 210, max_size=400)
        logo_font = pygame.font.Font(None, logo_font_size)
        logo_font.bold = True

        escape_text = "Нажмите Escape для выхода"

        score_text = f"Ваш счёт: {self.score}"
        best_score_text = f"Ваш лучший счёт для этого уровня: {self.best_score}"

        if self.score < MID_RESULT:
            final_text = "Не все получается с первого раза"
        elif self.score in range(MID_RESULT, HIGH_RESULT):
            final_text = "Ваш результат довольно неплох!"
        else:
            final_text = "Вы невероятно крутой!"

        text_font_size = get_font_size(self.width, self.height, 50)
        text_font = pygame.font.Font(None, text_font_size)

        offer_text = "Сыграйте еще раз, чтобы изменить свой результат!"

        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
            text_coord=0,
        )

        small_font_size = get_font_size(self.width, self.height, 30)
        small_font = pygame.font.Font(None, small_font_size)

        text_render_manager.render_as_text(
            escape_text,
            color="White",
            has_vertical_indent=False,
            font=small_font,
        )
        if self.error_text:
            text_render_manager.render_as_text(
                self.error_text,
                color="Red",
                has_vertical_indent=True,
                font=small_font,
            )

        text_render_manager.render_as_logo(logo_text, color="RED")

        text_render_manager.render_as_text(score_text)
        text_render_manager.render_as_text(best_score_text)
        text_render_manager.render_as_text(final_text)
        text_render_manager.render_as_text(offer_text)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
