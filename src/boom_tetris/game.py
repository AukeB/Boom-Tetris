""" " """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.polyomino.polyomino import Polyomino
from src.boom_tetris.renderer import Renderer
from src.boom_tetris.config.config import Config
from src.boom_tetris.configs.controls import SINGLE_PLAYER_CONTROLS as KEY


class Game:
    """ """

    def __init__(self, config: Config) -> None:
        """ """
        self.config = config

        pg.init()

        self.renderer = Renderer(config=self.config)
        self.board = Board(config=self.config)

        self.polyomino = Polyomino(
            self.board.dimensions.cols // 2, self.config.BOARD.DIMENSIONS.ROWS_HIDDEN
        )  # Probably correct.
        self.next_polyomino = Polyomino(self.board.dimensions.cols + 1, 1)

    def handle_controls(self, event) -> None:
        """ """
        if event.type == pg.KEYDOWN:
            # Horizontal and vertical movement.
            if event.key == KEY.UP:  # and not self.board.collision(
                #     self.polyomino, move_direction=self.config.DIRECTIONS.UP
                # ):
                self.polyomino.y += self.config.DIRECTIONS.UP[1]

            if event.key == KEY.DOWN:
                if not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.DOWN
                ):
                    self.polyomino.y += self.config.DIRECTIONS.DOWN[1]
                else:
                    self.get_next_polyomino()

            if event.key == KEY.LEFT and not self.board.collision(
                self.polyomino, move_direction=self.config.DIRECTIONS.LEFT
            ):
                self.polyomino.x += self.config.DIRECTIONS.LEFT[0]

            if event.key == KEY.RIGHT and not self.board.collision(
                self.polyomino, move_direction=self.config.DIRECTIONS.RIGHT
            ):
                self.polyomino.x += self.config.DIRECTIONS.RIGHT[0]

            # Rotational movement.
            if event.key == KEY.ROTATE_CLOCKWISE and not self.board.collision(
                self.polyomino, rotate_direction=self.config.DIRECTIONS.ROTATE_CLOCKWISE
            ):
                self.polyomino.rotate(self.config.DIRECTIONS.ROTATE_CLOCKWISE)

            if event.key == KEY.ROTATE_COUNTERCLOCKWISE and not self.board.collision(
                self.polyomino,
                rotate_direction=self.config.DIRECTIONS.ROTATE_COUNTERCLOCKWISE,
            ):
                self.polyomino.rotate(self.config.DIRECTIONS.ROTATE_COUNTERCLOCKWISE)

            # Optional hard-drop.
            if event.key == KEY.HARDDROP:
                while not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.DOWN
                ):
                    self.polyomino.y += self.config.DIRECTIONS.DOWN[1]

                self.get_next_polyomino()

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

    def get_next_polyomino(self):
        self.board.place(self.polyomino)
        self.board.clear_lines()
        self.next_polyomino.x, self.next_polyomino.y = (
            self.board.dimensions.cols // 2,
            self.config.BOARD.DIMENSIONS.ROWS_HIDDEN,
        )
        self.polyomino = self.next_polyomino
        self.next_polyomino = Polyomino(self.board.dimensions.cols + 1, 1)

    def update(self) -> callable:
        """ """
        with self.renderer:
            self.renderer.draw_board(board=self.board)
            self.renderer.draw_polyomino(self.polyomino, self.board.cell_rect.copy())
            self.renderer.draw_polyomino(
                self.next_polyomino, self.board.cell_rect.copy()
            )

        return self.handle_events()
