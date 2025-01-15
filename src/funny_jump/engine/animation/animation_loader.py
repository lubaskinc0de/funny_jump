from os import listdir
from pathlib import Path

import pygame


class AnimationFrameLoadError(Exception):
    ...


class IncrementalAnimationLoader:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load_frames(self) -> list[pygame.Surface]:
        frames: list[Path] = [self.path.joinpath(obj) for obj in listdir(self.path) if self.path.joinpath(obj).is_file()]

        try:
            sorted_frames = sorted(frames, key=lambda path: int(path.name.split(".")[0]))
        except ValueError as err:
            msg = f"Could not load frame from {self.path}, file-names must be integers"
            raise AnimationFrameLoadError(msg) from err

        img_frames = [pygame.image.load(frame) for frame in sorted_frames]
        return img_frames
