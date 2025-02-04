import json
import os
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from funny_jump.game.config import Config
from funny_jump.game.exception.base import BaseError
from funny_jump.game.level import Level


class ScoreReadError(BaseError):
    MESSAGE = "Ошибка чтения результата!"


class ScoreWriteError(BaseError):
    MESSAGE = "Ошибка сохранения результата!"


class ScoreStorage(Protocol):
    @abstractmethod
    def save_best_score(self, level: Level, score: int) -> None:
        ...

    @abstractmethod
    def get_best_score(self, level: Level) -> int:
        ...


@dataclass(slots=True, frozen=True)
class JsonScoreStorage(ScoreStorage):
    config: Config

    def save_best_score(self, level: Level, score: int) -> None:
        if not os.access(self.config.score_path, os.R_OK):
            raise ScoreWriteError

        if not os.access(self.config.score_path, os.W_OK):
            raise ScoreWriteError

        with self.config.score_path.open("r", encoding="utf-8") as fd:
            scores = json.load(fd)

            if not isinstance(scores, dict):
                raise ScoreWriteError

        with self.config.score_path.open("w", encoding="utf-8") as fd:
            scores[level.name.upper()] = score
            json.dump(scores, fd)

    def get_best_score(self, level: Level) -> int:
        if not os.access(self.config.score_path, os.R_OK):
            raise ScoreReadError

        with self.config.score_path.open("r", encoding="utf-8") as fd:
            scores: dict[str, int] = json.load(fd)

            if not isinstance(scores, dict):
                raise ScoreReadError

            level_name = level.name.upper()
            score = scores.get(level_name, 0)

            if isinstance(score, int) is False:
                raise ScoreReadError

            return score
