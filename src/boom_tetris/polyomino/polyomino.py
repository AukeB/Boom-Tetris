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
        self.properties = POLYOMINO_MAPPING[
            tuple((block.x, block.y) for block in self.blocks)
        ]
        self.rotation_type = self.properties["rotation_type"]

        if self.rotation_type == 1:
            self.rotation_index = 0
            self.rotations = [
                [Block(x, y) for x, y in rotation]
                for rotation in self.properties["rotations"]
            ]
            self.blocks = self.rotations[self.rotation_index]

    def rotate(self, direction: int) -> None:
        """ """
        if self.rotation_type == 1:
            # Ask chatgpt if this double code can be avoided somehow.
            self.rotation_index = (self.rotation_index + direction) % len(
                self.rotations
            )
            self.blocks = self.rotations[self.rotation_index]
        else:
            self.blocks = self.get_rotation(direction=direction)

    def get_rotation(self, direction: int) -> list[Block]:
        """ """
        if direction == 0:
            return self.blocks

        # If polyomino has None as rotation_type (such as the tetromino square),
        # do not perform rotational movement.
        if self.rotation_type is None:
            return self.blocks

        if self.rotation_type == 1:
            rotation_index = (self.rotation_index + direction) % len(self.rotations)
            return self.rotations[rotation_index]

        return [
            Block(-block.y * direction, block.x * direction) for block in self.blocks
        ]

    def __iter__(self) -> None:
        """ """
        return iter(self.blocks)
