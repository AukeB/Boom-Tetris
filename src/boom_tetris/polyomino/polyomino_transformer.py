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
        self.all_coordinates: list[tuple[tuple[int, int]]] = [
            tuple((x, y) for (x, y) in polyomino)
            for polyomino in config.POLYOMINO.ALL_SHAPES
        ]
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
        self, coordinate: list[list[int, int]], polyomino_mapping: dict[str, dict]
    ) -> dict[str, Any]:
        """ """
        # Convert to set for comparison.
        coordinate = set(map(tuple, coordinate))

        for polyomino_coordinates, polyomino_properties in polyomino_mapping.items():
            shape = set(map(tuple, polyomino_coordinates))

            if coordinate == shape:
                return polyomino_properties

        raise ValueError(f"No matching polyomino found for coordinates: {coordinate}")

    def _mirror_horizontally(
        self,
        coordinates: list[list[list[int, int]]],
    ) -> list[list[list[int, int]]]:
        """
        Needs to happen because positive y-direction of the board is
        downwards, while the positive y-direction in a polyomino
        definition is upwards.
        """
        mirrored_coordinates = [
            tuple((x, -y) for (x, y) in polyomino) for polyomino in coordinates
        ]

        return mirrored_coordinates

    def create_updated_polyomino_mapping(self, transformed_coordinates) -> dict:
        """ """
        polyomino_mapping_updated = {}

        for original_coordinates, transformed_coordinate in zip(
            self.all_coordinates, transformed_coordinates
        ):
            polyomino_mapping_updated[transformed_coordinate] = self.polyomino_mapping[
                original_coordinates
            ]

        return polyomino_mapping_updated

    def apply_rotation_point_shift(
        self,
        coordinates: list[list[list[int, int]]],
    ) -> list[list[list[int, int]]]:
        """ """
        all_new_coordinates = []

        for coordinate in coordinates:
            polyomino_properties = self._find_matching_polyomino(
                coordinate=coordinate, polyomino_mapping=self.polyomino_mapping
            )

            if polyomino_properties["rotation_type"] != 0:
                all_new_coordinates.append(coordinate)
                continue

            rotation_point = Position(*polyomino_properties["rotation_point"])

            shifted_coordinates = tuple(
                (x - rotation_point.x, y - rotation_point.y) for x, y in coordinate
            )

            all_new_coordinates.append(shifted_coordinates)

        return all_new_coordinates

    def execute(self) -> None:
        """ """
        rotated_coordinates = self.apply_rotation_point_shift(
            coordinates=self.all_coordinates
        )
        mirrored_coordinates = self._mirror_horizontally(
            coordinates=rotated_coordinates
        )
        polyomino_mapping_updated = self.create_updated_polyomino_mapping(
            transformed_coordinates=mirrored_coordinates
        )

        all_polyominos = self.convert_to_block_objects(
            all_coordinates=mirrored_coordinates
        )

        return all_polyominos, polyomino_mapping_updated
