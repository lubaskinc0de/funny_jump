from dataclasses import dataclass


@dataclass(slots=True)
class Button:
    name: str
    text: str

    width: int = 0
    height: int = 0

    left_top_x: int = 0
    left_top_y: int = 0

    color: str = "White"
    hovered_color: str = "Yellow"
    active_color: str = "Yellow4"
