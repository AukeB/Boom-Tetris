""" " """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.renderer import Renderer
from src.boom_tetris.constants import Dimensions
from src.boom_tetris.config_loader import Config
from src.boom_tetris.tetromino_generator import TetrominoGenerator


class Game:
    """ """

    def __init__(self, config: Config) -> None:
        """ """
        self.config = config

        pg.init()

        self.renderer = Renderer(
            config=self.config,
        )

        self.board = Board(
            dimensions=Dimensions(
                cols=self.config.BOARD.DIMENSIONS.COLS,
                rows=self.config.BOARD.DIMENSIONS.ROWS,
            ),
            rect=pg.Rect(
                self.config.BOARD.RECT.LEFT,
                self.config.BOARD.RECT.TOP,
                self.config.BOARD.RECT.WIDTH,
                self.config.BOARD.RECT.HEIGHT,
            ),
        )

        tetromino_generator = TetrominoGenerator(
            number_of_tetromino_cells=self.config.TETROMINO.SIZE
        )

        unique_tetrominos = tetromino_generator.generate()
        print(unique_tetrominos)

    def handle_events(self) -> bool:
        """ """
        for event in pg.event.get():
            if (
                event.type == pg.QUIT
                or event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE
            ):
                return False

        return True

    def update(self) -> callable:
        """ """
        with self.renderer:
            self.renderer.draw_board(board=self.board)

        return self.handle_events()
