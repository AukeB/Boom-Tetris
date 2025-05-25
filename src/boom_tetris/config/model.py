""" """

from pydantic import BaseModel, conint
from typing import Annotated

UInt8 = Annotated[int, conint(ge=0, le=255)]


class Polyomino(BaseModel):
    COLOR: tuple[UInt8, UInt8, UInt8]
    SIZE: int


class BoardCell(BaseModel):
    WIDTH: int
    HEIGHT: int


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
    CELL: BoardCell | None = None


class WindowColor(BaseModel):
    BACKGROUND: tuple[UInt8, UInt8, UInt8]


class Window(BaseModel):
    WIDTH: int
    HEIGHT: int
    COLOR: WindowColor


class ConfigModel(BaseModel):
    WINDOW: Window
    BOARD: Board
    TETROMINO: Polyomino
