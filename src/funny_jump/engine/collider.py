from pygame import Rect


def collider_top(other_rect: Rect, prev_pos: Rect, current_pos: Rect) -> bool:
    return (prev_pos.bottom <= other_rect.top) and (other_rect.top < current_pos.bottom)
