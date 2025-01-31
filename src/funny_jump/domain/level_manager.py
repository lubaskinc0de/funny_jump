from funny_jump.domain.entity.level import Level


class LevelManager:
    __slots__ = (
        "current_level_index",
        "levels",
    )

    def __init__(
        self,
    ) -> None:
        self.current_level_index: int = 0
        self.levels: list[Level] = self._init_levels()

    def _init_levels(self) -> list[Level]:
        first_level = Level(name="Trial", difficulty=0)
        second_level = Level(name="Base", difficulty=1)
        third_level = Level(name="Hard", difficulty=2)

        return [first_level, second_level, third_level]

    def change_level(self, level_number: int | None) -> None:
        self.current_level_index = level_number or self.current_level_index + 1

    def get_current_level(self) -> Level:
        return self.levels[self.current_level_index]
