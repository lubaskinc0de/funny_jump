from dataclasses import dataclass


@dataclass(slots=True)
class Level:
    name: str
    difficulty: int

    def __str__(self) -> str:
        return f"{self.name=} | {self.difficulty=}"
