""" """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.tetromino import Tetromino
from src.boom_tetris.config_loader import Config
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
            if board.cells[row][col].value:
                cell.x = board.rect.x + cell.width * col
                cell.y = board.rect.y + cell.height * row

                pg.draw.rect(
                    surface=self.surface,
                    color=self.config.TETROMINO.COLOR,
                    rect=cell,
                )

    def draw_tetromino(self, tetromino: Tetromino, block_rect: pg.Rect) -> None:
        """ """
        tetromino_position = Position(
            y=block_rect.y + tetromino.row * block_rect.height,
            x=block_rect.x + tetromino.col * block_rect.width,
        )

        print(block_rect.x, tetromino.col, block_rect.width)

        for block in tetromino:
            block_rect.y = tetromino_position.y + block.col * block_rect.width
            block_rect.x = tetromino_position.x + block.row * block_rect.height
            #print(block_rect)
            pg.draw.rect(self.surface, (self.config.TETROMINO.COLOR), block_rect)
