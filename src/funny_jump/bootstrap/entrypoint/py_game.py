import sys

import pygame.display

WIDTH = 340
HEIGHT = 460
CAPTION = "Весёлые Прыжки"


def pygame_main(_argv: list[str]) -> None:
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)


if __name__ == "__main__":
    pygame_main(sys.argv)
