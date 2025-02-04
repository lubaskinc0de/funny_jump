from collections.abc import Callable

import pygame
from pygame.event import Event

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.screen.base import BaseScreen
from funny_jump.game.text_manager import TextManager


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
        logo_font = pygame.font.Font(None, self.width // 3)
        logo_font.bold = True

        escape_text = "Нажмите Escape для выхода"

        score_text = f"Ваш результат - {self.score} очков"
        best_score_text = f"Ваш лучший результат для этого уровня - {self.best_score} очков"
        if self.score == 0:
            final_text = "Не все получается с первого раза"
        elif self.score < 50:
            final_text = "Ваш результат очень неплох!"
        else:
            final_text = "Вы достигли отличного результата!"
        text_font = pygame.font.Font(None, self.width // 11)

        offer_text = "Сыграйте еще раз, чтобы изменить свой результат!"

        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
            text_coord=0,
        )

        small_font = pygame.font.Font(None, self.width // 50)

        text_render_manager.render_as_text(
            escape_text,
            color="Gray10",
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
                    # След блок кода нужно будет изменить после добавления механики прохождения уровня
                    self.terminate()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
