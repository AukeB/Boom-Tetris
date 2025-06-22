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
    frames2ms,
)
from src.boom_tetris.configs.controls import SINGLE_PLAYER_CONTROLS as KEY


class Game:
    """ """

    def __init__(self, config: Config) -> None:
        """ """
        # General
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

        # Related to DAS (Delayed Auto Shift).
        self.clock = pg.time.Clock()
        self.frame_rate = self.config.GENERAL.NTSC_FRAMERATE
        self.das_delay = frames2ms(self.frame_rate, self.config.DAS.DAS_DELAY_NTSC)
        self.auto_repeat_rate = frames2ms(
            self.frame_rate, self.config.DAS.AUTO_REPEAT_RATE_NTSC
        )
        self.das_directions = self.config.DAS.DIRECTIONS
        self.key_pressed = {key: False for key in self.das_directions}
        self.hold_timer = {key: 0 for key in self.das_directions}

        # Related to lines cleared and level.
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

    def update_das(self, dt: int) -> None:
        """ """
        for direction in self.das_directions:
            if self.key_pressed[direction]:
                self.hold_timer[direction] += dt

                if self.hold_timer[direction] > self.das_delay:
                    move_direction = getattr(self.config.DIRECTIONS, direction)
                    if not self.board.collision(self.polyomino, move_direction):
                        if direction == "LEFT":
                            self.polyomino.x += move_direction[0]
                        if direction == "RIGHT":
                            self.polyomino.x += move_direction[0]
                        if direction == "DOWN":
                            self.polyomino.y += move_direction[1]

                        self.hold_timer[direction] = (
                            self.das_delay - self.auto_repeat_rate
                        )

                    else:
                        if direction == "DOWN":
                            self.get_next_polyomino()
                            self.key_pressed["DOWN"] = False
                            self.hold_timer["DOWN"] = 0
                else:
                    self.hold_timer[direction] = 0

    def handle_controls(self, event) -> None:
        """ """
        if event.type == pg.KEYDOWN:
            # Horizontal and vertical movement.
            if event.key == KEY.LEFT:
                self.key_pressed["LEFT"] = True
                self.hold_timer["LEFT"] = 0
                if not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.LEFT
                ):
                    self.polyomino.x += self.config.DIRECTIONS.LEFT[0]

            if event.key == KEY.RIGHT:
                self.key_pressed["RIGHT"] = True
                self.hold_timer["RIGHT"] = 0
                if not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.RIGHT
                ):
                    self.polyomino.x += self.config.DIRECTIONS.RIGHT[0]

            if event.key == KEY.DOWN:
                self.key_pressed["DOWN"] = True
                self.hold_timer["DOWN"] = 0
                if not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.DOWN
                ):
                    self.polyomino.y += self.config.DIRECTIONS.DOWN[1]
                else:
                    self.get_next_polyomino()

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

        elif event.type == pg.KEYUP:
            if event.key == KEY.LEFT:
                self.key_pressed["LEFT"] = False
                self.hold_timer["LEFT"] = 0
            elif event.key == KEY.RIGHT:
                self.key_pressed["RIGHT"] = False
                self.hold_timer["RIGHT"] = 0
            elif event.key == KEY.DOWN:
                self.key_pressed["DOWN"] = False
                self.hold_timer["DOWN"] = 0

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

        self.last_drop_time = pg.time.get_ticks()

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

        dt = self.clock.get_rawtime()

        self.update_das(dt)
        self.clock.tick(self.frame_rate)

        return self.handle_events()
