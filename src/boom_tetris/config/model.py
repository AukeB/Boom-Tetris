""" """

from pydantic import BaseModel, conint
from typing import Annotated, Literal

UInt8 = Annotated[int, conint(ge=0, le=255)]
IntDirection = Literal[-1, 0, 1]


class Directions(BaseModel):
    UP: list[IntDirection, IntDirection]
    DOWN: list[IntDirection, IntDirection]
    LEFT: list[IntDirection, IntDirection]
    RIGHT: list[IntDirection, IntDirection]
    ROTATE_CLOCKWISE: Literal[1, -1]
    ROTATE_COUNTERCLOCKWISE: Literal[1, -1]


class Polyomino(BaseModel):
    COLOR: list[UInt8, UInt8, UInt8]
    SIZE: int


class BoardCell(BaseModel):
    WIDTH: int
    HEIGHT: int


class BoardColor(BaseModel):
    BACKGROUND: list[UInt8, UInt8, UInt8]


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
    CELL: BoardCell | None = None


class WindowColor(BaseModel):
    BACKGROUND: list[UInt8, UInt8, UInt8]


class Window(BaseModel):
    WIDTH: int
    HEIGHT: int
    COLOR: WindowColor


class ConfigModel(BaseModel):
    WINDOW: Window
    BOARD: Board
    POLYOMINO: Polyomino
    DIRECTIONS: Directions
