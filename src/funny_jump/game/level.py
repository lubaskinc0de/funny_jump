from dataclasses import dataclass


@dataclass(slots=True)
class Level:
    name: str
    difficulty: int
