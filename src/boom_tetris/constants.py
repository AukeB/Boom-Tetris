""" """

from collections import namedtuple

MAIN_CONFIG_RELATIVE_FILE_PATH = "src/boom_tetris/configs/main_config.yaml"

Position = namedtuple("Position", "x y")

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
