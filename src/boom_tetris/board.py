""" """

import itertools
import pygame as pg


from src.boom_tetris.constants import Dimensions


class BoardCell:
    """ """

    def __init__(
        self,
        row: int,
        col: int,
        value: int,
    ) -> None:
        """ """
        self.row = row
        self.col = col
        self.value = value


class Board:
    """ """

    def __init__(
        self,
        dimensions: Dimensions,
        rect: pg.Rect,
    ) -> None:
        """ """
        self.dimensions = dimensions
        self.rect = rect
        self.cells: list[list[int]] = [
            [BoardCell(row, col, 0) for col in range(self.dimensions.cols)]
            for row in range(self.dimensions.rows)
        ]

        cell_width = self.rect.width // self.dimensions.cols
        cell_height = self.rect.height // self.dimensions.rows
        self.cell_rect = pg.Rect(self.rect.left, self.rect.top, cell_width, cell_height)

    def __iter__(self):
        """ """
        return itertools.product(
            range(self.dimensions.rows), range(self.dimensions.cols)
        )
