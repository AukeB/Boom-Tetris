""" """

import yaml

from pydantic import BaseModel, conint
from typing import Annotated


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


class ConfigModel(BaseModel):
    WINDOW: Window
    BOARD: Board
    TETROMINO: Tetromino


class Config:
    """ """

    def __init__(self, config_path: str) -> None:
        """ """
        self.config_path = config_path

    def load_main_config(self, file_type: str = "yaml") -> dict:
        """ """
        if file_type == "yaml":
            with open(self.config_path) as file:
                main_config = yaml.load(file, Loader=yaml.FullLoader)

            config = ConfigModel(**main_config)

        return config

    def augment_config(self, config: ConfigModel) -> ConfigModel:
        """ """
        pass
