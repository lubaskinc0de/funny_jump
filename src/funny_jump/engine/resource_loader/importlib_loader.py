from abc import ABC
from dataclasses import dataclass
from importlib.abc import Traversable
from pathlib import Path

from funny_jump.engine.resource_loader.base import ResourceLoader, ResourceLoadError


@dataclass(slots=True, frozen=True)
class ImportLibResourceLoader(ResourceLoader, ABC):
    resources_dir: Traversable

    def get_full_path(self, relative_path: Path) -> Path:
        traversable_path = self.resources_dir / str(relative_path)
        path = Path(str(traversable_path))

        if not path.exists():
            raise ResourceLoadError

        return path
