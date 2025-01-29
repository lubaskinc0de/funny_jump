from collections.abc import Callable
from functools import partial
from pathlib import Path

import pygame
from pygame import Surface

from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.text_manager import TextManager
from funny_jump.game.screen.base import BaseScreen


class EndScreen(BaseScreen):
    __slots__ = (
        "asset_manager",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "logo_font_size",
        "resource_loader",
        "screen",
        "terminate",
        "text_coord",
        "text_font_size",
        "text_render_manager",
        "width",
        "score",
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
        logo_text = "КОНЕЦ"
        logo_font = pygame.font.Font(None, 160)
        logo_font.bold = True

        score_text = f"Ваш результат - {self.score} очков"
        if self.score == 0:
            final_text = "Не все получается с первого раза"
        elif self.score < 50:
            final_text = "Ваш результат очень неплох!"
        else:
            final_text = "Вы достигли отличного результата!"
        text_font = pygame.font.Font(None, 70)

        offer_text = "Сыграйте еще раз, чтобы изменить свой результат!"
        
        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
        )

        text_render_manager.render_as_logo(logo_text, color="RED")
        text_render_manager.render_as_text(score_text, has_vertical_indent=True)
        text_render_manager.render_as_text(final_text, has_vertical_indent=True)
        text_render_manager.render_as_text(offer_text, has_vertical_indent=True)