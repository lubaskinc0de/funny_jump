def get_font_size(width: int, height: int, base_size: int, min_size: int = 10, max_size: int = 100) -> int:
    screen_min_side = min(width, height)
    font_size = int(base_size * screen_min_side / 1000)

    return max(min_size, min(font_size, max_size))
