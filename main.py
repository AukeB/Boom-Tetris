""" """

from src.boom_tetris.game import Game
from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import MAIN_CONFIG_RELATIVE_FILE_PATH


def main() -> None:
    """ """
    config_manager = Config(config_path=MAIN_CONFIG_RELATIVE_FILE_PATH)
    main_config = config_manager.load_main_config()

    game = Game(config=main_config)

    while game.update():
        pass


if __name__ == "__main__":
    main()
