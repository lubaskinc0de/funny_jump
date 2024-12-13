import sys

from funny_jump.bootstrap.entrypoint.py_game import pygame_main


def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        return

    try:
        module = argv[0]
        option = argv[1]
        args = argv[2:]
    except IndexError:
        return

    modules = {
        "run": {
            "game": pygame_main,
        },
    }

    if module not in modules:
        return

    if option not in modules[module]:
        return

    modules[module][option](args)
