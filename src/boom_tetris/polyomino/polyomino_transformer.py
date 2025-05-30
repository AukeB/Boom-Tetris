""" """

import json
from typing import Any

from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.constants import (
    Position,
    Block,
    TETROMINO_PROPERTIES_RELATIVE_FILE_PATH,
)


class PolyominoTransformer:
    """ """

    def __init__(self, config: ConfigModel):
        """ """
        self.all_coordinates: list[list[list[int, int]]] = config.POLYOMINO.ALL_SHAPES
        self.polyomino_size: int = config.POLYOMINO.SIZE
        self.polyomino_mapping: dict = self._load_polyomino_properties()

    def _load_polyomino_properties(
        self,
    ) -> dict:
        """ """
        if self.polyomino_size == 4:
            with open(TETROMINO_PROPERTIES_RELATIVE_FILE_PATH, "r") as file:
                polyomino_mapping = json.load(file)

            # Because the coordinate representation of the polyomino is used in
            # str format as key of the dictionary, we need to convert it to a tuple.
            polyomino_mapping = {
                tuple(map(tuple, json.loads(k))): v
                for k, v in polyomino_mapping.items()
            }

        return polyomino_mapping

    def convert_to_block_objects(
        self, all_coordinates: list[list[list[int, int]]]
    ) -> list[list[Block]]:
        """ """
        all_polyominos = []

        for coordinates in all_coordinates:
            polyomino = [Block(x, y) for x, y in coordinates]
            all_polyominos.append(polyomino)

        return all_polyominos

    def _find_matching_polyomino(
        self, coordinates: list[list[int, int]], polyomino_mapping: dict[str, dict]
    ) -> dict[str, Any]:
        """ """
        # Convert to set for comparison.
        coordinates = set(map(tuple, coordinates))

        for polyomino_coordinates, polyomino_properties in polyomino_mapping.items():
            shape = set(map(tuple, polyomino_coordinates))

            if coordinates == shape:
                return polyomino_properties

        raise ValueError(f"No matching polyomino found for coordinates: {coordinates}")

    def apply_rotation_point_shift(
        self,
    ) -> list[list[list[int, int]]]:
        """ """
        all_new_coordinates = []
        polyomino_mapping_rotated = {}

        for coordinates in self.all_coordinates:
            polyomino_properties = self._find_matching_polyomino(
                coordinates=coordinates, polyomino_mapping=self.polyomino_mapping
            )

            if polyomino_properties["rotation_type"] != 0:
                all_new_coordinates.append(coordinates)
                coordinates = tuple((x, y) for x, y in coordinates)
                polyomino_mapping_rotated[coordinates] = polyomino_properties
                continue

            rotation_point = Position(*polyomino_properties["rotation_point"])

            shifted_coordinates = tuple(
                (x - rotation_point.x, y - rotation_point.y) for x, y in coordinates
            )

            all_new_coordinates.append(shifted_coordinates)
            polyomino_mapping_rotated[shifted_coordinates] = polyomino_properties

        return all_new_coordinates, polyomino_mapping_rotated

    def execute(self) -> None:
        """ """
        shifted_coordinates, polyomino_mapping_rotated = (
            self.apply_rotation_point_shift()
        )

        all_polyominos = self.convert_to_block_objects(
            all_coordinates=shifted_coordinates
        )

        return all_polyominos, polyomino_mapping_rotated
