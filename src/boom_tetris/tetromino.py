""" """

from src.boom_tetris.constants import Block


class Tetromino:
    """ """

    def __init__(self, row: int, col: int) -> None:
        """ """
        self.row, self.col = row, col
        self.blocks = [
            Block(0, -1),
            Block(0, 0),
            Block(0, 1),
            Block(1, 0),
        ]  # T-block.

    def rotate(self, direction: int) -> None:
        """ """
        self.blocks = [
            Block(block.col * direction, -block.row * direction)
            for block in self.blocks
        ]

    def __iter__(self) -> None:
        """ """
        return iter(self.blocks)
