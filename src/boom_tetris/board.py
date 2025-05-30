""" """

import itertools
import pygame as pg

from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.constants import Dimensions, Position
from src.boom_tetris.polyomino.polyomino import Polyomino


class Board:
    """ """

    def __init__(
        self,
        config: ConfigModel,
    ) -> None:
        """ """
        self.config = config

        self.dimensions = Dimensions(
            rows=self.config.BOARD.DIMENSIONS.ROWS,
            cols=self.config.BOARD.DIMENSIONS.COLS,
        )
        self.rect = pg.Rect(
            self.config.BOARD.RECT.LEFT,
            self.config.BOARD.RECT.TOP,
            self.config.BOARD.RECT.WIDTH,
            self.config.BOARD.RECT.HEIGHT,
        )

        self.cells: list[list[int]] = [
            [0 for _ in range(self.dimensions.cols)]
            for _ in range(self.dimensions.rows)
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
        move_direction: Position[int, int] = Position(0, 0),
        rotate_direction: int = 0,
    ) -> None:
        """ """
        for block in polyomino.get_rotation(rotate_direction):
            boundary_position = Position(
                x=polyomino.x + block.x + move_direction.x,
                y=polyomino.y + block.y + move_direction.y,
            )

            # Collision with board edge.
            collision: bool = (
                boundary_position.x < 0
                or boundary_position.x >= self.dimensions.cols
                # or boundary_position.y < 0
                or boundary_position.y >= self.dimensions.rows
            )

            if collision:
                return True

            # Collision with other pieces.
            if self.cells[boundary_position.y][boundary_position.x]:
                return True

        return False

    def place(self, polyominal: Polyomino) -> None:
        """ """
        for block in polyominal:
            self.cells[polyominal.y + block.y][polyominal.x + block.x] = 1

    def clear_lines(self) -> None:
        """ """
        for row in self.cells[:]:
            if 0 not in row:
                self.cells.remove(row)
                self.cells.insert(0, [0] * self.dimensions.cols)

    def __iter__(self):
        """ """
        return itertools.product(
            range(self.dimensions.rows), range(self.dimensions.cols)
        )
