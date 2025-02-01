from dataclasses import dataclass


@dataclass(slots=True)
class Level:
    name: str
    difficulty: int
    passed: bool = False

    def __str__(self) -> str:
        return f"{self.name=} | {self.difficulty=} {self.passed=}"
