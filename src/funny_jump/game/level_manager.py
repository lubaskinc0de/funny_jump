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
        first_level = Level(name="Trial", difficulty=0)
        second_level = Level(name="Base", difficulty=1)

        self.levels = [first_level, second_level]

    def change_level(self, level_index: int) -> None:
        self.current_level_index = level_index

    def get_current_level(self) -> Level:
        return self.levels[self.current_level_index]
