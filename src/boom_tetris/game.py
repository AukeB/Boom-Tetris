""" " """

import pygame as pg

from src.boom_tetris.board import Board
from src.boom_tetris.polyomino.polyomino import Polyomino
from src.boom_tetris.renderer import Renderer
from src.boom_tetris.config.config import Config
from src.boom_tetris.utils.game_utils import (
    convert_drop_frames_to_time,
    compute_first_level_advancement,
    get_frames_per_cell,
)
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
            self.config.POLYOMINO.SPAWN_POSITION[0],
            self.config.POLYOMINO.SPAWN_POSITION[1],
        )
        self.next_polyomino = Polyomino(
            self.config.POLYOMINO.SPAWN_POSITION_NEXT[0],
            self.config.POLYOMINO.SPAWN_POSITION_NEXT[1],
        )

        self.level = 0
        self.leveled_up = False
        self.line_threshold_first_level_advancement = compute_first_level_advancement(
            self.level
        )

        self.line_counter = 0
        self.last_drop_time = pg.time.get_ticks()

        # Probably best to merge these two functions.
        frames_per_cell = get_frames_per_cell(
            self.level, self.config.GENERAL.NTSC_DROP_FRAMES
        )

        self.drop_interval = convert_drop_frames_to_time(
            framerate=self.config.GENERAL.NTSC_FRAMERATE,
            frames_per_cell=frames_per_cell,
        )

    def handle_controls(self, event) -> None:
        """ """
        if event.type == pg.KEYDOWN:
            # Horizontal and vertical movement.
            if event.key == KEY.UP and not self.board.collision(
                self.polyomino, move_direction=self.config.DIRECTIONS.UP
            ):
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

    def update_lines_and_level(self, lines_cleared: int) -> None:
        """ """
        if not self.leveled_up:
            if (
                self.line_counter + lines_cleared
                >= self.line_threshold_first_level_advancement
            ):
                self.level += 1
                self.leveled_up = True
        else:
            if (self.line_counter + lines_cleared) // 10 != self.line_counter // 10:
                self.level += 1

        self.line_counter += lines_cleared

    def get_next_polyomino(self):
        """ """
        # Place the polyomino on the board.
        self.board.place(self.polyomino)

        # Possible update line clear, level and drop speed.
        lines_cleared = self.board.clear_lines()
        self.update_lines_and_level(lines_cleared=lines_cleared)

        if self.level in self.config.GENERAL.NTSC_DROP_FRAMES:
            self.drop_interval = convert_drop_frames_to_time(
                framerate=self.config.GENERAL.NTSC_FRAMERATE,
                frames_per_cell=self.config.GENERAL.NTSC_DROP_FRAMES[self.level],
            )

        self.next_polyomino.x, self.next_polyomino.y = (
            self.config.POLYOMINO.SPAWN_POSITION[0],
            self.config.POLYOMINO.SPAWN_POSITION[1],
        )
        self.polyomino = self.next_polyomino
        self.next_polyomino = Polyomino(
            self.config.POLYOMINO.SPAWN_POSITION_NEXT[0],
            self.config.POLYOMINO.SPAWN_POSITION_NEXT[1],
        )

    def handle_timers(self):
        """ """
        current_time = pg.time.get_ticks()

        if current_time - self.last_drop_time >= self.drop_interval:
            if not self.board.collision(
                self.polyomino, move_direction=self.config.DIRECTIONS.DOWN
            ):
                self.polyomino.y += self.config.DIRECTIONS.DOWN[1]
            else:
                self.get_next_polyomino()
            self.last_drop_time = current_time

    def update(self) -> callable:
        """ """
        with self.renderer:
            self.renderer.draw_board(board=self.board)
            self.renderer.draw_polyomino(self.polyomino, self.board.cell_rect.copy())
            self.renderer.draw_polyomino(
                self.next_polyomino, self.board.cell_rect.copy()
            )

            self.renderer.draw_grid_lines(board=self.board)
            self.renderer.draw_block_hidden_rows(board=self.board)

        self.handle_timers()

        return self.handle_events()
