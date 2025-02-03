from dataclasses import dataclass

from funny_jump.game.difficulty_parameters import DifficultyParameters


@dataclass(slots=True)
class Level:
    name: str
    difficulty_parameters: DifficultyParameters
