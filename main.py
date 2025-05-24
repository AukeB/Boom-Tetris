""" """

from src.boom_tetris.game import Game
from src.boom_tetris.config_loader import load_main_config


def main() -> None:
    """ """
    main_config = load_main_config()

    game = Game(config=main_config)

    while game.update():
        pass


if __name__ == "__main__":
    main()
