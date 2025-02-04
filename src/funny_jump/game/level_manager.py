from funny_jump.game.difficulty_parameters import DifficultyParameters
from funny_jump.game.level import Level


class LevelManager:
    __slots__ = (
        "current_level_index",
        "levels",
    )

    def __init__(self) -> None:
        self.current_level_index: int = 0
        self.levels: list[Level]
        self._init_levels()

    def _init_levels(self) -> None:
        first_level = Level(
            name="Trial",
            difficulty_parameters=DifficultyParameters(platform_x_moving_chance=0.0),
            )
        second_level = Level(
            name="Base",
            difficulty_parameters=DifficultyParameters(),
            )
        third_level = Level(
            name="Max",
            difficulty_parameters=DifficultyParameters(
                all_platforms_y_moving_speed=0.75,
                ),
        )

        self.levels = [first_level, second_level, third_level]

    def change_level(self, level_index: int | None = None) -> None:
        if level_index is None:
            self.current_level_index = self.current_level_index + 1
        else:
            self.current_level_index = level_index

    def get_current_level(self) -> Level:
        return self.levels[self.current_level_index]
