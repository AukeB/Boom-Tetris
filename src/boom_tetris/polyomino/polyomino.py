""" """

import random as rd

from src.boom_tetris.constants import Block
from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH
from src.boom_tetris.polyomino.polyomino_transformer import PolyominoTransformer

config_main = Config.load_config(
    file_path=MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH, validate=False
)

polyomino_transformer = PolyominoTransformer(config=config_main)

ALL_POLYOMINOS, POLYOMINO_MAPPING = polyomino_transformer.execute()


class Polyomino:
    """ """

    def __init__(self, x: int, y: int) -> None:
        """ """
        self.x = x
        self.y = y

        polyomino_index = rd.randint(0, len(ALL_POLYOMINOS) - 1)

        self.blocks = ALL_POLYOMINOS[polyomino_index]
        print(self.blocks)
        print(
            POLYOMINO_MAPPING[tuple((block.x, block.y) for block in self.blocks)][
                "name"
            ]
        )

        # print(self.blocks)

        # for key, _ in POLYOMINO_MAPPING.items():
        #     print(key)

        # if POLYOMINO_MAPPING[tuple((block.x, block.y) for block in self.blocks)]:
        #     print(POLYOMINO_MAPPING[tuple((block.x, block.y) for block in self.blocks)]["name"])

    def rotate(self, direction: int) -> None:
        """ """
        self.blocks = self.get_rotation(direction=direction)

    def get_rotation(self, direction: int) -> list[Block]:
        """ """
        if direction == 0:
            return self.blocks

        return [
            Block(-block.y * direction, block.x * direction) for block in self.blocks
        ]

    def __iter__(self) -> None:
        """ """
        return iter(self.blocks)
