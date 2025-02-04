from dataclasses import dataclass


@dataclass(slots=True)
class DifficultyParameters:
    platform_x_moving_speed: float = 2.5
    platform_x_moving_chance: float = 0.1

    all_platforms_y_moving_speed: float = 0.0
