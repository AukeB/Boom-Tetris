""" """

from src.boom_tetris.game import Game
from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import MAIN_CONFIG_RELATIVE_FILE_PATH


def main() -> None:
    """ """
    config_main = Config.load_config(file_path=MAIN_CONFIG_RELATIVE_FILE_PATH)

    config_instance = Config(config_path=MAIN_CONFIG_RELATIVE_FILE_PATH)
    config_augmented = config_instance.augment_config(config=config_main)

    game = Game(config=config_augmented)

    while game.update():
        pass


if __name__ == "__main__":
    main()
