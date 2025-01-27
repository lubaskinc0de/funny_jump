import pygame

from funny_jump.domain.value_object.bounds import Bounds
from funny_jump.domain.entity.player import Player
from funny_jump.domain.service.platform_collide import on_player_collide_platform
from funny_jump.game.sprites.platform import PlatformSprite
from funny_jump.game.sprites.player import PlayerSprite
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.game.path_to_assets import Asset

LN = None
class CollisionManager:
    __slots__ = (
        "platforms",
        "player",
        "player_sprite",
        "screen",
        "prev_position",
        "asset_manager",
        "last_ff",
    )

    def __init__(
        self,
        player_sprite: PlayerSprite,
        platforms: pygame.sprite.Group,  # type: ignore  # noqa: PGH003
        player: Player,
        screen: pygame.Surface,
        asset_manager: AssetManager[Asset] = None
    ) -> None:
        self.player_sprite: PlayerSprite = player_sprite
        self.platforms = platforms
        self.player = player
        self.screen = screen
        self.prev_position: Bounds = self.player.bounds
        self.asset_manager = asset_manager
        self.last_ff: float = 0

    def check_collisions(self) -> None:
        self._check_player_collides_platforms()

    # def _check_player_collides_platforms(self) -> None:
    #     player_rect = self.player_sprite.rect
    #     # ray = pygame.Rect()
    #     collide: list[PlatformSprite] = pygame.sprite.spritecollide(
    #         self.player_sprite,
    #         self.platforms,
    #         dokill=False,
    #     )

    #     if not collide and self.player.on_ground:
    #         self.player.left_from_ground()
    #         return

    #     if not collide:
    #         return

    #     if self.player.on_ground:
    #         return

    #     for platform_sprite in collide:
    #         platform_rect = platform_sprite.rect
    #         prev_bottom = player_rect.bottom - self.player.velocity.y

    #         if (prev_bottom <= platform_rect.top) and (platform_rect.top < player_rect.bottom):
    #             self.player_sprite.set_position(
    #                 player_rect.centerx,
    #                 (platform_rect.top - player_rect.height // 2) + 2,
    #             )
    #             on_player_collide_platform(platform_sprite.platform, self.player)
    #             self.prev_player_position = self.player_sprite.player.bounds
    #             return
    
    def _check_player_collides_platforms(self) -> None:
        player_rect = self.player_sprite.rect
        current_position = player_rect.center

        prev_position = self.prev_position

        line_start = (prev_position.center_x, prev_position.center_y)
        line_end = (current_position[0], current_position[1])

        collide: list[PlatformSprite] = pygame.sprite.spritecollide(
            self.player_sprite,
            self.platforms,
            dokill=False,
        )

        if not collide and self.player.on_ground:
            self.player.left_from_ground()
            return

        if not collide:
            return

        if self.player.on_ground:
            return

        for platform_sprite in collide:
            platform_rect = platform_sprite.rect

            if self._line_rect_collision(line_start, line_end, platform_rect):
                self.player_sprite.set_position(
                    player_rect.centerx,
                    (platform_rect.top - player_rect.height // 2) + 2,
                )
                on_player_collide_platform(platform_sprite.platform, self.player)
                return

        self.prev_position = Bounds(current_position[0], current_position[1], player_rect.width, player_rect.height)

    def _line_rect_collision(
        self,
        line_start: tuple[float, float], 
        line_end: tuple[float, float],
        rect: pygame.Rect
        ) -> bool:
        
        rect_left = rect.left
        rect_right = rect.right
        rect_top = rect.top
        rect_bottom = rect.bottom
        if self._lines_intersect(line_start, line_end, (rect_left, rect_top), (rect_left, rect_bottom)):  # левая сторона
            return True
        if self._lines_intersect(line_start, line_end, (rect_left, rect_top), (rect_right, rect_top)):  # верхняя сторона
            return True
        if self._lines_intersect(line_start, line_end, (rect_right, rect_top), (rect_right, rect_bottom)):  # правая сторона
            return True
        if self._lines_intersect(line_start, line_end, (rect_left, rect_bottom), (rect_right, rect_bottom)):  # нижняя сторона
            return True

        return False
    
    def _lines_intersect(
        self, 
        line_start1: tuple[float, float], 
        line_end1: tuple[float, float], 
        line_start2: tuple[float, float], 
        line_end2: tuple[float, float]
        ) -> bool:
        
        def is_counter_clockwise(
            point_a: tuple[float, float],
            point_b: tuple[float, float], 
            point_c: tuple[float, float]
            ) -> bool:
            return (point_c[1] - point_a[1]) * (point_b[0] - point_a[0])\
                > (point_b[1] - point_a[1]) * (point_c[0] - point_a[0])

        return (
            is_counter_clockwise(line_start1, line_start2, line_end2)\
                != is_counter_clockwise(line_end1, line_start2, line_end2) and
            is_counter_clockwise(line_start1, line_end1, line_start2)\
                != is_counter_clockwise(line_start1, line_end1, line_end2)
                )

