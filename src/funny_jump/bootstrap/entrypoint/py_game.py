import logging
import sys
from importlib.resources import files

import funny_jump.game.assets
from funny_jump.engine.asset_manager import AssetManager
from funny_jump.engine.resource_loader.importlib_loader import ImportLibResourceLoader
from funny_jump.engine.screen import get_screen_size
from funny_jump.game.config import load_from_file
from funny_jump.game.game_director import GameDirector
from funny_jump.game.path_to_assets import ASSET_PATH
from funny_jump.game.score.score_storage import JsonScoreStorage

sys_width, sys_height = get_screen_size()
WIDTH = int(sys_width * 0.5)
HEIGHT = sys_height - 100

CAPTION = "Весёлые Прыжки"
FPS = 60
VSYNC = True

logging.basicConfig(level=0)


def pygame_main(_argv: list[str]) -> None:
    resource_loader = ImportLibResourceLoader(files(funny_jump.game.assets))
    asset_manager = AssetManager(loader=resource_loader, path_to_assets=ASSET_PATH)
    config = load_from_file()
    score_storage = JsonScoreStorage(config)

    game_fps = FPS

    if _argv and _argv[0] and _argv[0].isdigit():
        game_fps = int(_argv[0])

    director = GameDirector(
        fps=game_fps,
        width=WIDTH,
        height=HEIGHT,
        caption=CAPTION,
        vsync=VSYNC,
        resource_loader=resource_loader,
        asset_manager=asset_manager,
        score_storage=score_storage,
    )

    logging.info("Startup..")
    director.run_game()


if __name__ == "__main__":
    pygame_main(sys.argv)
