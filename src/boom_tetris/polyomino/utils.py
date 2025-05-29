""" """

import json

from pathlib import Path

from src.boom_tetris.constants import Block


def convert_all_polyominos_to_block_objects(
    all_coordinates: list[list[list[int, int]]],
) -> list[list[Block]]:
    """ """
    all_polyominos = []

    for coordinates in all_coordinates:
        polyomino = [Block(x, y) for x, y in coordinates]
        all_polyominos.append(polyomino)

    return all_polyominos


def find_matching_polyomino(coordinates, polyomino_mapping):
    """ """
    # Convert to set for comparison.
    coordinates = set(map(tuple, coordinates))

    for polyomino_name, polyomino_properties in polyomino_mapping.items():
        shape = set(map(tuple, polyomino_properties["shape"]))

        if coordinates == shape:
            return polyomino_name, polyomino_properties


def apply_linear_transformation(
    all_coordinates: list[list[list[int, int]]],
) -> list[list[list[int, int]]]:
    """ """
    if len(all_coordinates[0]) == 4:
        with open(Path("src/boom_tetris/configs/tetrominos.json"), "r") as file:
            polyomino_mapping = json.load(file)

    new_all_coordinates = []

    for coordinates in all_coordinates:
        polyomino_name, polyomino_properties = find_matching_polyomino(
            coordinates=coordinates, polyomino_mapping=polyomino_mapping
        )

        rotation_point = polyomino_properties["rotation_point"]

        print(polyomino_name)
        print(coordinates)

        if not rotation_point:
            new_all_coordinates.append(coordinates)
            continue

        shifted_coordinates = []

        for x, y in coordinates:
            shifted_x = x - rotation_point[0]
            shifted_y = y - rotation_point[1]

            shifted_coordinates.append([shifted_x, shifted_y])

        print(shifted_coordinates)

        new_all_coordinates.append(shifted_coordinates)

    return new_all_coordinates
