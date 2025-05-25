""" """

import random as rd

from src.boom_tetris.constants import Block
from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import CONFIG_POLYOMINOS_RELATIVE_FILE_PATH
from src.boom_tetris.polyomino.utils import convert_all_polyominos_to_block_objects

config_polyomino = Config.load_config(
    file_path=CONFIG_POLYOMINOS_RELATIVE_FILE_PATH, validate=False
)

ALL_POLYOMINOS = convert_all_polyominos_to_block_objects(
    all_coordinates=config_polyomino.ALL_POLYOMINOS
)


class Polyomino:
    """ """

    def __init__(self, x: int, y: int) -> None:
        """ """
        self.x = x
        self.y = y
        choice = rd.randint(0, len(ALL_POLYOMINOS) - 1)
        self.blocks = ALL_POLYOMINOS[choice]

    def rotate(self, direction: int) -> None:
        """ """
        self.blocks = self.get_rotation(direction=direction)

    def get_rotation(self, direction: int) -> list[Block]:
        """ """
        if direction == 0:
            return self.blocks

        return [
            Block(block.x * direction, -block.y * direction) for block in self.blocks
        ]

    def __iter__(self) -> None:
        """ """
        return iter(self.blocks)
