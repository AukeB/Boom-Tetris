""" """

from collections import namedtuple
from pathlib import Path

# Main configuration relative file path.
MAIN_CONFIG_RELATIVE_FILE_PATH = Path("src/boom_tetris/configs/main_config.yaml")
MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH = Path(
    "src/boom_tetris/configs/main_config_augmented.yaml"
)

# Polyomino properpties paths.
TETROMINO_PROPERTIES_RELATIVE_FILE_PATH = Path(
    "src/boom_tetris/configs/tetromino_properties.json"
)

"""
`Dimensions` refers to the structural properties of a grid, 
    matrix, or layout, specifying the number of columns and 
    rows into which the grid is partitioned.
`Size` denotes the physical or spatial extent of an object,
    characterized by its width and height. These measurements
    are typically expressed in pixels, but any unit of physical 
    distance may be employed.
`Position` specifies a location using `x` and `y` coordinates.
    These coordinates may represent a position on the screen 
    in pixel units, or a location within a grid or board, 
    expressed in terms of columns and rows.
`Block` defines the discrete position of a unit cell within a 
    polyomino, specified by its `x` and `y` within a local 
    grid. It is used to describe the shape and structure of a 
    tetromino or other polyomino piece.
"""
Dimensions = namedtuple("Dimensions", "rows cols")
Size = namedtuple("Size", "width height")
Position = namedtuple("Position", "x y")
Block = namedtuple("Block", "x y")
