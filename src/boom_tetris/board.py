""" """

import itertools
import pygame as pg

from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.constants import Dimensions, Position
from src.boom_tetris.polyomino import Polyomino


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

    def collision(
        self,
        polyomino: Polyomino,
        move_direction: tuple[int, int] = Position(0, 0),
        rotate_direction: int = 0,
    ) -> None:
        """ """
        for block in polyomino.get_rotation(rotate_direction):
            boundary_position = Position(
                y=polyomino.y + block.y + move_direction.y,
                x=polyomino.x + block.x + move_direction.x,
            )

            # Collision with board edge.
            collision: bool = (
                boundary_position.x < 0
                or boundary_position.x >= self.dimensions.cols
                or boundary_position.y < 0
                or boundary_position.y >= self.dimensions.rows
            )

            if collision:
                return True

            # Collision with other pieces.
            if self.cells[boundary_position.y][boundary_position.x].value:
                return True

        return False

    def __iter__(self):
        """ """
        return itertools.product(
            range(self.dimensions.rows), range(self.dimensions.cols)
        )
