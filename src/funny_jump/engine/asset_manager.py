from collections.abc import Callable
from pathlib import Path
from typing import Any, Generic, TypeVar

from funny_jump.engine.resource_loader.base import ResourceLoader

T = TypeVar("T")
AssetT = TypeVar("AssetT")


class AssetManager(Generic[AssetT]):
    __slots__ = ("_cache", "loader", "path_to_assets")

    def __init__(self, loader: ResourceLoader, path_to_assets: dict[AssetT, Path]) -> None:
        self._cache: dict[AssetT, Any] = {}
        self.loader = loader
        self.path_to_assets = path_to_assets

    def get_asset(self, asset: AssetT, asset_loader: Callable[[Path], T]) -> T:
        if asset in self._cache:
            return self._cache[asset]  # type: ignore  # noqa: PGH003

        full_path = self.loader.get_full_path(self.path_to_assets[asset])
        resource: T = asset_loader(full_path)
        self._cache[asset] = resource

        return resource

    def get_asset_path(self, asset: AssetT) -> Path:
        return self.loader.get_full_path(self.path_to_assets[asset])
