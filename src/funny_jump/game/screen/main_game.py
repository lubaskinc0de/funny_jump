from collections.abc import Callable

import pygame
from pygame.event import Event

from funny_jump.domain.entity.player import Player
from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.value_object.velocity import Velocity
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.font import get_font_size
from funny_jump.engine.resource_loader.base import ResourceLoader
from funny_jump.game.level_manager import LevelManager
from funny_jump.game.path_to_assets import Asset
from funny_jump.game.score.score_storage import ScoreStorage
from funny_jump.game.screen.base import BaseScreen
from funny_jump.game.sprite_manager import SpriteManager
from funny_jump.game.text_manager import TextManager


class MainGameScreen(BaseScreen):
    __slots__ = (
        "asset_manager",
        "assets",
        "clock",
        "fps",
        "get_bg",
        "height",
        "is_running",
        "level_manager",
        "player",
        "resource_loader",
        "score",
        "score_storage",
        "screen",
        "sprite_manager",
        "terminate",
        "width",
    )

    def __init__(
        self,
        *,
        fps: int,
        width: int,
        height: int,
        resource_loader: ResourceLoader,
        asset_manager: AssetManager[Asset],
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        terminate: Callable[[], None],
        level_manager: LevelManager,
        score_storage: ScoreStorage,
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
        self.sprite_manager: SpriteManager
        self.level_manager = level_manager
        self.is_running = False
        self.player: Player
        self.score_storage = score_storage
        self.score = 0

    def refresh_all_sprites(self) -> None:
        self.player = Player(
            screen_h=self.height,
            screen_w=self.width,
            bounds=Bounds(),
            velocity=Velocity(),
        )
        self.sprite_manager = SpriteManager(
            screen=self.screen,
            width=self.width,
            height=self.height,
            resource_loader=self.resource_loader,
            asset_manager=self.asset_manager,
            level_manager=self.level_manager,
            player=self.player,
        )

    def render_all(self) -> None:
        escape_text = "Нажмите Escape для выхода"
        text_font = pygame.font.Font(None, get_font_size(self.width, self.height, 25))

        text_render_manager = TextManager(
            text_font=text_font,
            screen_width=self.width,
            screen=self.screen,
            text_coord=0,
        )

        text_render_manager.render_as_text(
            escape_text,
            color="white",
            has_vertical_indent=False,
        )

        text_render_manager.render_as_score(
            score=f"Счёт: {self.score}",
            font=pygame.font.Font(None, get_font_size(self.width, self.height, 50)),
        )

    def _run_main_loop(self) -> None:
        pygame.mixer.music.load(self.asset_manager.get_asset_path(Asset.GAME_BG_MUSIC))
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        pygame.mixer.music.set_volume(0.2)

        self.refresh_all_sprites()

        delta = 0.0
        while self.is_running:
            self._dispatch_events(pygame.event.get())
            self.sprite_manager.update(delta)

            if self.player.health <= 0:
                break

            self.load_bg()

            self.sprite_manager.draw()
            self.score = self.sprite_manager.player_score
            self.render_all()

            pygame.display.flip()
            delta = self.clock.tick(self.fps) / 1000

        level = self.level_manager.get_current_level()
        if self.score > self.score_storage.get_best_score(level):
            self.score_storage.save_best_score(level, self.score)

    def _dispatch_events(self, events: list[Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False
                    self.terminate()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
