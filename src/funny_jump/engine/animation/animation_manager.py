from abc import abstractmethod
from dataclasses import dataclass
from typing import NewType, Protocol, TypeAlias

import pygame

AnimationId = NewType("AnimationId", str)


class AnimatedSprite(Protocol):
    @abstractmethod
    def set_new_image(self, new_img: pygame.Surface) -> None: ...

    @abstractmethod
    def animation_end(self) -> None: ...


@dataclass(slots=True, frozen=True)
class Animation:
    animation_id: AnimationId
    frames: list[pygame.Surface]
    duration: float

    def __hash__(self) -> int:
        return hash(self.animation_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Animation):
            return False
        return self.animation_id == other.animation_id


Animations: TypeAlias = dict[AnimationId, Animation]


class AnimationManager(Protocol):
    @abstractmethod
    def apply(self, sprite: AnimatedSprite, animation: AnimationId) -> None: ...

    @abstractmethod
    def update(self, delta: float) -> None: ...


class AnimationManagerDummy(AnimationManager):
    animations: Animations

    def __init__(self, animations: Animations) -> None:
        self.animations = animations
        self._reset()

    def _reset(self) -> None:
        self.is_running = False
        self.current_animation: Animation | None = None
        self.time_from_start = 0.0
        self.frame_time = 0.0
        self.last_frame_time = 0.0
        self.current_frames: list[pygame.Surface] = []
        self.frame_idx = 0
        self.sprite: AnimatedSprite | None = None

    def apply(self, sprite: AnimatedSprite, animation: AnimationId) -> None:
        self._reset()

        self.current_animation = self.animations[animation]
        self.current_frames = self.current_animation.frames
        self.frame_time = self.current_animation.duration / len(self.current_frames)
        self.is_running = True
        self.sprite = sprite

    def update(self, delta: float) -> None:
        if not self.is_running or self.sprite is None or self.current_animation is None:
            return

        if self.frame_idx >= len(self.current_frames):
            self.sprite.animation_end()
            self._reset()
            return

        self.time_from_start += delta

        if self.last_frame_time == 0.0:
            self.sprite.set_new_image(self.current_frames[0])
            self.last_frame_time = self.time_from_start
            self.frame_idx += 1
        elif self.time_from_start - self.last_frame_time >= self.frame_time:
            self.sprite.set_new_image(self.current_frames[self.frame_idx])
            self.last_frame_time = self.time_from_start
            self.frame_idx += 1
