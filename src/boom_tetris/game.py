""" " """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.tetromino import Tetromino
from src.boom_tetris.renderer import Renderer
from src.boom_tetris.config.config import Config
from src.boom_tetris.tetromino_generator import TetrominoGenerator


class Game:
    """ """

    def __init__(self, config: Config) -> None:
        """ """
        self.config = config

        pg.init()

        self.renderer = Renderer(config=self.config)
        self.board = Board(config=self.config)

        tetromino_generator = TetrominoGenerator(
            number_of_tetromino_cells=self.config.TETROMINO.SIZE
        )

        unique_tetrominos = tetromino_generator.generate()
        print(unique_tetrominos)
        self.tetromino = Tetromino(row=0, col=self.board.dimensions.cols // 2)

    def handle_controls(self, event) -> None:
        """ """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.tetromino.col -= 1
            if event.key == pg.K_RIGHT:
                self.tetromino.col += 1
            if event.key == pg.K_DOWN:
                self.tetromino.row += 1
            if event.key == pg.K_UP:
                self.tetromino.row -= 1

            if event.key == pg.K_a:
                self.tetromino.rotate(-1)
            if event.key == pg.K_d:
                self.tetromino.rotate(1)

    def handle_events(self) -> bool:
        """ """
        for event in pg.event.get():
            if (
                event.type == pg.QUIT
                or event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE
            ):
                return False

            self.handle_controls(event)

        return True

    def update(self) -> callable:
        """ """
        with self.renderer:
            self.renderer.draw_board(board=self.board)
            self.renderer.draw_tetromino(self.tetromino, self.board.cell_rect.copy())

        return self.handle_events()
