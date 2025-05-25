""" """

from collections import namedtuple
from pathlib import Path

MAIN_CONFIG_RELATIVE_FILE_PATH = Path("src/boom_tetris/configs/main_config.yaml")

# Used for exact position, with `y` and `x` having
# pixel number as unit.
Position = namedtuple("Position", "y x")

"""
`Dimensions` refers to the structural properties of a grid, 
    matrix, or layout, specifying the number of columns and 
    rows into which the grid is partitioned.
`Size` denotes the physical or spatial extent of an object,
    characterized by its width and height. These measurements
    are typically expressed in pixels, but any unit of physical 
    distance may be employed.
"""
Dimensions = namedtuple("Dimensions", "cols rows")
Size = namedtuple("Size", "width height")

# Used for defining Tetromino's.
Block = namedtuple("Block", "row col")
