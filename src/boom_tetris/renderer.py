""" """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.polyomino.polyomino import Polyomino
from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import Position


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

        cell = board.cell_rect.copy()

        for row, col in board:
            if board.cells[row][col]:
                cell.x = board.rect.x + board.cell_rect.width * col
                cell.y = board.rect.y + board.cell_rect.height * row

                pg.draw.rect(
                    surface=self.surface,
                    color=self.config.POLYOMINO.COLOR,
                    rect=cell,
                )

    def draw_polyomino(self, polyomino: Polyomino, block_rect: pg.Rect) -> None:
        """ """
        polyomino_position = Position(
            x=block_rect.x + polyomino.x * block_rect.width,
            y=block_rect.y + polyomino.y * block_rect.height,
        )

        for block in polyomino:
            block_rect.y = polyomino_position.y + block.y * block_rect.height
            block_rect.x = polyomino_position.x + block.x * block_rect.width
            pg.draw.rect(self.surface, (self.config.POLYOMINO.COLOR), block_rect)
