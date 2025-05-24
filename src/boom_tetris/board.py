""" """

import itertools
import random as rd
import pygame as pg


from src.boom_tetris.constants import Dimensions


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
            [rd.randint(0, 1) for _ in range(self.dimensions.cols)]
            for _ in range(self.dimensions.rows)
        ]

    def __iter__(self):
        """ """
        return itertools.product(
            range(self.dimensions.rows), range(self.dimensions.cols)
        )
