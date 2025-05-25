""" """

import pygame as pg

from src.boom_tetris.utils.dot_dict import DotDict

SINGLE_PLAYER_CONTROLS = DotDict(
    {
        "LEFT": pg.K_a,
        "RIGHT": pg.K_d,
        "UP": pg.K_w,
        "DOWN": pg.K_s,
        "ROTATE_CLOCKWISE": pg.K_RIGHT,
        "ROTATE_COUNTERCLOCKWISE": pg.K_LEFT,
        "HARDDROP": pg.K_SPACE,
    }
)
