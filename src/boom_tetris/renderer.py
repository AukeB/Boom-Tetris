""" """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.config_loader import Config
from src.boom_tetris.constants import Size


class Renderer:
    """ """

    def __init__(
        self,
        config: Config,
    ) -> None:
        """ """
        self.config = config
        self.window_width = self.config.WINDOW.WIDTH
        self.window_height = self.config.WINDOW.HEIGHT
        self.background_color = self.config.WINDOW.COLOR.BACKGROUND

        board_cell_width = (
            self.config.BOARD.RECT.WIDTH // self.config.BOARD.DIMENSIONS.COLS
        )
        board_cell_height = (
            self.config.BOARD.RECT.HEIGHT // self.config.BOARD.DIMENSIONS.ROWS
        )

        self.board_cell = Size(width=board_cell_width, height=board_cell_height)

        self._initialize_window()

        self.surface = pg.display.get_surface()

    def __enter__(self) -> None:
        """ """
        self.surface.fill(color=self.background_color)

    def __exit__(self, exc_tupe, exc_value, exc_trace) -> None:
        """ """
        pg.display.update()

    def _initialize_window(self) -> None:
        """ """
        pg.display.set_mode(size=(self.window_width, self.window_height))

    def draw_board(self, board: Board) -> None:
        """ """
        pg.draw.rect(
            surface=self.surface,
            color=self.config.BOARD.COLOR.BACKGROUND,
            rect=board.rect,
        )

        cell = pg.Rect(0, 0, self.board_cell.width, self.board_cell.height)

        for row, col in board:
            if board.cells[row][col]:
                cell.x = board.rect.x + cell.width * col
                cell.y = board.rect.y + cell.height * row

                pg.draw.rect(
                    surface=self.surface,
                    color=self.config.TETROMINO.COLOR,
                    rect=cell,
                )
