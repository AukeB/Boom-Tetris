""" """

from pydantic import BaseModel, ConfigDict, conint
from typing import Annotated, Literal

UInt8 = Annotated[int, conint(ge=0, le=255)]
IntDirection = Literal[-1, 0, 1]


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Directions(StrictBaseModel):
    UP: list[IntDirection, IntDirection]
    DOWN: list[IntDirection, IntDirection]
    LEFT: list[IntDirection, IntDirection]
    RIGHT: list[IntDirection, IntDirection]
    ROTATE_CLOCKWISE: Literal[1, -1]
    ROTATE_COUNTERCLOCKWISE: Literal[1, -1]


class Polyomino(StrictBaseModel):
    COLOR: list[UInt8, UInt8, UInt8]
    SIZE: int
    ALL_SHAPES: list | None = None
    SPAWN_POSITION: list[int, int] | None = None
    SPAWN_POSITION_NEXT: list[int, int] | None = None


class BoardGridLines(StrictBaseModel):
    ENABLED: bool
    LINE_COLOR: list[UInt8, UInt8, UInt8]
    LINE_WIDTH: int


class BoardCell(StrictBaseModel):
    WIDTH: int | float
    HEIGHT: int | float


class BoardColor(StrictBaseModel):
    BACKGROUND: list[UInt8, UInt8, UInt8]


class BoardRect(StrictBaseModel):
    LEFT: int | float | None = None
    TOP: int | float | None = None
    WIDTH: int | float | None = None
    HEIGHT: int | float | None = None


class BoardDimensions(StrictBaseModel):
    ROWS: int
    COLS: int
    ROWS_HIDDEN: int
    ROWS_TOTAL: int | None = None


class Board(StrictBaseModel):
    DIMENSIONS: BoardDimensions
    RECT: BoardRect | None = None
    COLOR: BoardColor
    CELL: BoardCell | None = None
    GRID_LINES: BoardGridLines


class WindowColor(StrictBaseModel):
    BACKGROUND: list[UInt8, UInt8, UInt8]


class Window(StrictBaseModel):
    WIDTH: int
    HEIGHT: int
    MARGIN: int
    COLOR: WindowColor


class ConfigModel(StrictBaseModel):
    WINDOW: Window
    BOARD: Board
    POLYOMINO: Polyomino
    DIRECTIONS: Directions
