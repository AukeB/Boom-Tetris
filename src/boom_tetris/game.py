""" " """

import os
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
    gravity2ms,
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
        self.das_directions = self.config.DAS.DIRECTIONS

        self.key_pressed = {key: False for key in self.das_directions}
        self.hold_timer = {key: 0 for key in self.das_directions}

        self.soft_drop_speed = gravity2ms(
            self.frame_rate, self.config.GENERAL.SOFT_DROP_SPEED
        )
        self.das_delay = {
            direction: frames2ms(self.frame_rate, self.config.DAS.DAS_DELAY_NTSC)
            for direction in self.das_directions
        }

        self.auto_repeat_rate = {
            direction: frames2ms(self.frame_rate, self.config.DAS.AUTO_REPEAT_RATE_NTSC)
            for direction in self.das_directions
        }

        # Manual correction for soft drop speed.
        self.das_delay["DOWN"] = self.soft_drop_speed
        self.auto_repeat_rate["DOWN"] = self.soft_drop_speed

        # ARE delay (Automatic Repeat Entry delay)
        self.are_delay = frames2ms(self.frame_rate, self.config.GENERAL.ARE_DELAY)
        self.in_are = False
        self.are_timer = 0

        # Related to lines cleared and level.
        self.level = self.config.GENERAL.START_LEVEL
        self.leveled_up = False
        self.line_threshold_first_level_advancement = compute_first_level_advancement(
            self.level
        )

        self.line_counter = 0
        self.last_drop_time = pg.time.get_ticks()

        # Related to scoring
        self.score = 0
        self.score_dict = self.initialize_scoring_dictionary()

        # Probably best to merge these two functions.
        frames_per_cell = get_frames_per_cell(
            self.level, self.config.GENERAL.NTSC_DROP_FRAMES
        )

        self.drop_interval = convert_drop_frames_to_time(
            framerate=self.config.GENERAL.NTSC_FRAMERATE,
            frames_per_cell=frames_per_cell,
        )

    def initialize_scoring_dictionary(self) -> dict:
        """ """
        single_points = self.config.SCORE.SINGLE
        double_points = single_points * self.config.SCORE.DOUBLE_MULTIPLIER
        triple_points = double_points * self.config.SCORE.TRIPLE_MULTIPLIER
        tetris_points = triple_points * self.config.SCORE.TETRIS_MULTIPLIER

        score_dict = {
            1: single_points,
            2: double_points,
            3: triple_points,
            4: tetris_points,
        }

        return score_dict

    def update_key_hold(self, direction: str, is_pressed: bool) -> None:
        """ """
        self.key_pressed[direction] = is_pressed
        self.hold_timer[direction] = 0

    def update_das(self, dt: int) -> None:
        """ """
        for direction in self.das_directions:
            if self.key_pressed[direction]:
                self.hold_timer[direction] += dt
                move_direction = getattr(self.config.DIRECTIONS, direction)

                if not self.board.collision(self.polyomino, move_direction):
                    if self.hold_timer[direction] > self.das_delay[direction]:
                        if direction in ["LEFT", "RIGHT"]:
                            self.polyomino.x += move_direction[0]
                        if direction == "DOWN":
                            self.polyomino.y += move_direction[1]

                        self.hold_timer[direction] = (
                            self.das_delay[direction] - self.auto_repeat_rate[direction]
                        )
                else:
                    if direction in ["LEFT", "RIGHT"]:
                        self.hold_timer[direction] = self.das_delay[direction] + 1
                    elif direction == "DOWN":
                        self.get_next_polyomino()
                        self.update_key_hold(direction, is_pressed=True)
            else:
                self.hold_timer[direction] = 0

    def handle_controls(self, event) -> None:
        """ """
        if event.type == pg.KEYDOWN:
            # Horizontal and vertical movement.
            if event.key == KEY.LEFT:
                self.update_key_hold("LEFT", is_pressed=True)
                if not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.LEFT
                ):
                    self.polyomino.x += self.config.DIRECTIONS.LEFT[0]

            if event.key == KEY.RIGHT:
                self.update_key_hold("RIGHT", is_pressed=True)
                if not self.board.collision(
                    self.polyomino, move_direction=self.config.DIRECTIONS.RIGHT
                ):
                    self.polyomino.x += self.config.DIRECTIONS.RIGHT[0]

            if event.key == KEY.DOWN:
                self.update_key_hold("DOWN", is_pressed=True)
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
                self.update_key_hold("LEFT", is_pressed=False)
            elif event.key == KEY.RIGHT:
                self.update_key_hold("RIGHT", is_pressed=False)
            elif event.key == KEY.DOWN:
                self.update_key_hold("DOWN", is_pressed=False)

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

    def update_score(self, level: int, lines_cleared: int):
        """ """
        score_to_add = (level + 1) * self.score_dict[lines_cleared]
        self.score += score_to_add

    def get_next_polyomino(self):
        """ """
        # Place the polyomino on the board.
        self.board.place(self.polyomino)

        # Possible update line clear, level and drop speed.
        lines_cleared = self.board.clear_lines()

        if lines_cleared:
            self.update_score(level=self.level, lines_cleared=lines_cleared)
            self.update_lines_and_level(lines_cleared=lines_cleared)

        os.system("clear")
        print(f"{self.score=}")
        print(f"{self.line_counter=}")
        print(f"{self.level=}")

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

        if not self.key_pressed["DOWN"]:
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
        self.update_das(dt=self.clock.tick(self.frame_rate))

        return self.handle_events()
