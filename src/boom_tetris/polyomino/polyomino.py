""" """

import random as rd

from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH
from src.boom_tetris.polyomino.polyomino_transformer import PolyominoTransformer, PolyominoTransformer2

config_main = Config.load_config(
    file_path=MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH, validate=False
)

#polyomino_transformer = PolyominoTransformer(config=config_main)

#ALL_POLYOMINOS, POLYOMINO_MAPPING = polyomino_transformer.execute()

polyomino_transformer_2 = PolyominoTransformer2(config=config_main)
ALL_POLYOMINOS2, POLYOMINO_MAPPING2 = polyomino_transformer_2.execute()

class Polyomino:
    """ """

    def __init__(self, x: int, y: int) -> None:
        """ """
        self.x = x
        self.y = y

        polyomino_index = rd.randint(0, len(ALL_POLYOMINOS2) - 1)

        self.blocks = ALL_POLYOMINOS2[polyomino_index]
        self.properties = POLYOMINO_MAPPING2[tuple(tuple(block) for block in self.blocks)]
        print(self.properties.name)
        self.rotation_type = self.properties.rotation_type

        if self.rotation_type == "predefined":
            self.rotation_index = 0
            self.rotations = self.properties.rotations
            self.blocks = self.rotations[self.rotation_index]

    def rotate(self, direction: int) -> None:
        """ """
        if self.rotation_type == "predefined":
            # Ask chatgpt if this double code can be avoided somehow.
            self.rotation_index = (self.rotation_index + direction) % len(
                self.rotations
            )
            self.blocks = self.rotations[self.rotation_index]
        else:
            self.blocks = self.get_rotation(direction=direction)

    def get_rotation(self, direction: int) -> list[tuple]:
        """ """
        if direction == 0:
            return self.blocks

        # If polyomino has None as rotation_type (such as the tetromino square),
        # do not perform rotational movement.
        if self.rotation_type is None:
            return self.blocks

        if self.rotation_type == "predefined":
            rotation_index = (self.rotation_index + direction) % len(self.rotations)
            return self.rotations[rotation_index]

        return [(-y * direction, x * direction) for (x, y) in self.blocks]

    def __iter__(self) -> None:
        """ """
        return iter(self.blocks)
