import json
from dataclasses import dataclass
from pathlib import Path

BASE_PATH = Path(Path.expanduser(Path("~/funny_jump/")))
SCORE_PATH = Path(BASE_PATH / "score.json")


@dataclass(slots=True, frozen=True)
class Config:
    score_path: Path


def load_from_file() -> Config:
    if not BASE_PATH.exists():
        BASE_PATH.mkdir(parents=True)

    if not SCORE_PATH.exists():
        with SCORE_PATH.open("w") as fd:
            json.dump({}, fd)

    return Config(
        score_path=SCORE_PATH,
    )
