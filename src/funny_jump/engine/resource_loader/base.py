from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class ResourceLoadError(Exception): ...


class ResourceLoader(Protocol):
    @abstractmethod
    def get_full_path(self, relative_path: Path) -> Path: ...
