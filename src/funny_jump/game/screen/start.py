import pygame
from pygame.event import Event

from funny_jump.game.screen.base import BaseScreen
from funny_jump.game.text_manager import TextManager


class StartScreen(BaseScreen):
    def render_all(self) -> None:
        logo_text = "FUNNY JUMP"
        logo_font = pygame.font.Font(None, self.width // 5)
        logo_font.bold = True

        intro_text = "Нажмите на любую клавишу мыши, чтобы начать"
        text_font = pygame.font.Font(None, self.width // 11)

        text_render_manager = TextManager(
            text_font=text_font,
            logo_font=logo_font,
            screen_width=self.width,
            screen=self.screen,
        )

        text_render_manager.render_as_logo(logo_text)
        text_render_manager.render_as_text(intro_text)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame.MOUSEBUTTONDOWN:
                    self.is_running = False
