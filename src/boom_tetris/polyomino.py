""" """

from src.boom_tetris.constants import Block


class Polyomino:
    """ """

    def __init__(self, y: int, x: int, all_polyominos: list) -> None:
        """ """
        self.y, self.x = y, x

        self.all_polyominos = all_polyominos

        self.blocks = self.all_polyominos[4]

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
