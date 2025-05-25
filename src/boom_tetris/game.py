""" " """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.polyomino import Polyomino
from src.boom_tetris.renderer import Renderer
from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import Position
from src.boom_tetris.polyomino_generator import PolyominoGenerator


class Game:
    """ """

    def __init__(self, config: Config) -> None:
        """ """
        self.config = config

        pg.init()

        self.renderer = Renderer(config=self.config)
        self.board = Board(config=self.config)

        polyomino_generator = PolyominoGenerator(
            number_of_polyomino_cells=self.config.TETROMINO.SIZE
        )

        unique_polyominos = polyomino_generator.generate()

        self.polyomino = Polyomino(
            y=0, x=self.board.dimensions.cols // 2, all_polyominos=unique_polyominos
        )

    def handle_controls(self, event) -> None:
        """ """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT and not self.board.collision(
                self.polyomino, move_direction=Position(0, -1)
            ):
                self.polyomino.x -= 1
            if event.key == pg.K_RIGHT and not self.board.collision(
                self.polyomino, move_direction=Position(0, 1)
            ):
                self.polyomino.x += 1
            if event.key == pg.K_DOWN and not self.board.collision(
                self.polyomino, move_direction=Position(1, 0)
            ):
                self.polyomino.y += 1
            if event.key == pg.K_UP and not self.board.collision(
                self.polyomino, move_direction=Position(-1, 0)
            ):
                self.polyomino.y -= 1

            if event.key == pg.K_a and not self.board.collision(
                self.polyomino, rotate_direction=-1
            ):
                self.polyomino.rotate(-1)
            if event.key == pg.K_d and not self.board.collision(
                self.polyomino, rotate_direction=1
            ):
                self.polyomino.rotate(1)

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
            self.renderer.draw_polyomino(self.polyomino, self.board.cell_rect.copy())

        return self.handle_events()
