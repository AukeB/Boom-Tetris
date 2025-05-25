""" """

import itertools
import pygame as pg

from src.boom_tetris.config.model import ConfigModel
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
        config: ConfigModel,
    ) -> None:
        """ """
        self.config = config

        self.dimensions = Dimensions(
            cols=self.config.BOARD.DIMENSIONS.COLS,
            rows=self.config.BOARD.DIMENSIONS.ROWS,
        )
        self.rect = pg.Rect(
            self.config.BOARD.RECT.LEFT,
            self.config.BOARD.RECT.TOP,
            self.config.BOARD.RECT.WIDTH,
            self.config.BOARD.RECT.HEIGHT,
        )

        self.cells: list[list[int]] = [
            [BoardCell(row, col, 0) for col in range(self.dimensions.cols)]
            for row in range(self.dimensions.rows)
        ]

        self.cell_rect = pg.Rect(
            self.rect.left,
            self.rect.top,
            self.config.BOARD.CELL.WIDTH,
            self.config.BOARD.CELL.HEIGHT,
        )

    def __iter__(self):
        """ """
        return itertools.product(
            range(self.dimensions.rows), range(self.dimensions.cols)
        )
