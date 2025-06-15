""" """

import json
from typing import Any

from src.boom_tetris.utils.dict_utils import DotDict
from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.constants import (
    Position,
    TETROMINO_PROPERTIES_RELATIVE_FILE_PATH,
)

class PolyominoTransformer2:
    """ """
    def __init__(self, config: ConfigModel):
        """ """
        self.polyominos: list[list[list[int, int]]] = config.POLYOMINO.ALL_SHAPES
        self.polyomino_size = config.POLYOMINO.SIZE
        self.polyomino_mapping: dict = self._load_polyomino_properties()
        self._sort()
    
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

            # Because the dictionary keys are tuples, apply the DotDict one level deeper.
            for polyomino_index in polyomino_mapping:
                polyomino_mapping[polyomino_index] = DotDict(polyomino_mapping[polyomino_index])

        return polyomino_mapping
    
    def _sort(
        self,
    ) -> list[list[list[int, int]]]:
        """ """
        # Sort the polyominos.
        self.polyominos = list(sorted(sorted(polyomino) for polyomino in self.polyominos))

        # Sort the polyomino mapping.
        sorted_polyomino_mapping = {}

        for k, _ in self.polyomino_mapping.items():
            sorted_key = tuple(sorted(k))
            sorted_polyomino_mapping[sorted_key] = self.polyomino_mapping[k]
            
        self.polyomino_mapping = dict(sorted(sorted_polyomino_mapping.items()))
        
    def _rotate(
        self,
    ) -> None:
        """ """
        updated_polyomino_mapping = {}

        for i, (polyomino, (polyomino_index, polyomino_properties)) in enumerate(zip(self.polyominos, self.polyomino_mapping.items())):
            if "rotation_correction" in polyomino_properties and polyomino_properties.rotation_correction != 0:
                rotated_polyomino = [[-y * polyomino_properties.rotation_correction, x * polyomino_properties.rotation_correction] for [x, y] in polyomino]
                
                self.polyominos[i] = rotated_polyomino
                updated_polyomino_mapping[tuple(tuple(block) for block in rotated_polyomino)] = polyomino_properties
            else:
                updated_polyomino_mapping[tuple(tuple(block) for block in polyomino)] = polyomino_properties

        self.polyomino_mapping = updated_polyomino_mapping

        self._sort()
    
    def _shift(
        self,
    ) -> None:
        """ """
        updated_polyomino_mapping = {}

        for i, (polyomino, (polyomino_index, polyomino_properties)) in enumerate(zip(self.polyominos, self.polyomino_mapping.items())):
            if "position_correction" in polyomino_properties and any(x != 0 for x in polyomino_properties.position_correction):
                shifted_polyomino = [[x + polyomino_properties.position_correction[0], y + polyomino_properties.position_correction[1]] for [x, y] in polyomino]

                self.polyominos[i] = shifted_polyomino
                updated_polyomino_mapping[tuple(tuple(block) for block in shifted_polyomino)] = polyomino_properties
            else:
                updated_polyomino_mapping[tuple(tuple(block) for block in polyomino)] = polyomino_properties

        self.polyomino_mapping = updated_polyomino_mapping

        self._sort()
    
    def _mirror_horizontally(
        self,
    ) -> list[list[list[int, int]]]:
        """
        Needs to happen because positive y-direction of the board is
        downwards, while the positive y-direction in a polyomino
        definition is upwards.
        """
        updated_polyomino_mapping = {}

        for i, (polyomino, (polyomino_index, polyomino_properties)) in enumerate(zip(self.polyominos, self.polyomino_mapping.items())):
            mirrored_polyomino = [[x, -y] for [x, y] in polyomino]

            self.polyominos[i] = mirrored_polyomino
            updated_polyomino_mapping[tuple(tuple(block) for block in mirrored_polyomino)] = polyomino_properties
        
        self.polyomino_mapping = updated_polyomino_mapping
        
        self._sort()
    
    def execute(
        self
    ):
        """ """
        

        # for polyomino, (polyomino_index, polyomino_properties) in zip(self.polyominos, self.polyomino_mapping.items()):
        #     print(polyomino)
        #     print(polyomino_index)
        #     print(polyomino_properties.name)
        #     print()


        self._rotate()
        self._shift()
        self._mirror_horizontally()

        # print('\n'*5)

        # for polyomino, (polyomino_index, polyomino_properties) in zip(self.polyominos, self.polyomino_mapping.items()):
        #     print(polyomino)
        #     print(polyomino_index)
        #     print(polyomino_properties.name)
        #     print()
        
        return self.polyominos, self.polyomino_mapping



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

        # Because the dictionary keys are tuples, apply the DotDict one level deeper.
        for polyomino_index in polyomino_mapping:
            polyomino_mapping[polyomino_index] = DotDict(polyomino_mapping[polyomino_index])


        return polyomino_mapping
    
    def _sort_polyominos(
        self,
        polyominos: list[list[list[int, int]]] | dict[tuple, dict]
    ) -> list[list[list[int, int]]]:
        """ """
        if isinstance(polyominos, list):
            sorted_polyominos = list(sorted(sorted(polyomino) for polyomino in polyominos))
        elif isinstance(polyominos, dict):
            sorted_polyominos = dict(sorted(polyominos.items()))

        return sorted_polyominos

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
        coordinates: list[list[list[int, int]]]
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
    
    def _apply_linear_transformations(
        self,
        coordinates: list[list[list[int, int]]],
        polyomino_mapping: dict,
    ) -> list[list[list[int, int]]]:
        """ """
        shifted_coordinates = []

        # Possible to make sure indices are aligned so you don't need double loop?
        for polyomino in coordinates:
            for polyomino_index, polyomino_properties in polyomino_mapping.items():
                if polyomino == polyomino_index:
                    horizontal = polyomino_mapping[polyomino_index].position_correction[0]
                    vertical = polyomino_mapping[polyomino_index].position_correction[1]

                    if horizontal == 0 and vertical == 0:
                        shifted_coordinates.append(polyomino)
                    else:
                        shifted_coordinate = tuple(
                            (x + horizontal, y + vertical) for (x, y) in polyomino
                        )

                        shifted_coordinates.append(shifted_coordinate)


        return shifted_coordinates

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

            if polyomino_properties.rotation_type != "matrix_rotation":
                all_new_coordinates.append(coordinate)
                continue

            rotation_point = Position(*polyomino_properties.rotation_point)

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

        polyomino_mapping_updated = self.create_updated_polyomino_mapping(
            transformed_coordinates=rotated_coordinates
        )

        shifted_coordinates = self._apply_linear_transformations(
            coordinates=rotated_coordinates,
            polyomino_mapping=polyomino_mapping_updated
        )

        mirrored_coordinates = self._mirror_horizontally(
            coordinates=shifted_coordinates,
        )

        polyomino_mapping_updated = self.create_updated_polyomino_mapping(
            transformed_coordinates=mirrored_coordinates
        )

        return mirrored_coordinates, polyomino_mapping_updated



"""
j-piece             
l_piece             
t_piece             
longbar             DONE
squiggly            DONE
reverse_squiggly    
square              DONE
"""