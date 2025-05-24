""" """

import yaml

from pydantic import BaseModel, conint
from typing import Annotated

from src.boom_tetris.constants import MAIN_CONFIG_RELATIVE_FILE_PATH

UInt8 = Annotated[int, conint(ge=0, le=255)]


class Tetromino(BaseModel):
    COLOR: tuple[UInt8, UInt8, UInt8]
    SIZE: int


class BoardColor(BaseModel):
    BACKGROUND: tuple[UInt8, UInt8, UInt8]


class BoardRect(BaseModel):
    LEFT: int
    TOP: int
    WIDTH: int
    HEIGHT: int


class BoardDimensions(BaseModel):
    ROWS: int
    COLS: int


class Board(BaseModel):
    DIMENSIONS: BoardDimensions
    RECT: BoardRect
    COLOR: BoardColor


class WindowColor(BaseModel):
    BACKGROUND: tuple[UInt8, UInt8, UInt8]


class Window(BaseModel):
    WIDTH: int
    HEIGHT: int
    COLOR: WindowColor


class Config(BaseModel):
    WINDOW: Window
    BOARD: Board
    TETROMINO: Tetromino


def load_main_config(file_type: str = "yaml") -> dict:
    """ """
    if file_type == "yaml":
        with open(MAIN_CONFIG_RELATIVE_FILE_PATH) as file:
            main_config = yaml.load(file, Loader=yaml.FullLoader)

        config = Config(**main_config)

    return config
