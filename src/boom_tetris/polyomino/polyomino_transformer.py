""" """

import json

from src.boom_tetris.utils.dict_utils import DotDict
from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.constants import (
    TETROMINO_PROPERTIES_RELATIVE_FILE_PATH,
)


class PolyominoTransformer:
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
        if self.polyomino_size == 3:
            pass
        elif self.polyomino_size == 4:
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
                polyomino_mapping[polyomino_index] = DotDict(
                    polyomino_mapping[polyomino_index]
                )

            return polyomino_mapping
        else:
            pass

    def _sort(
        self,
    ) -> list[list[list[int, int]]]:
        """ """
        # Sort the polyominos.
        self.polyominos = list(
            sorted(sorted(polyomino) for polyomino in self.polyominos)
        )

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

        for i, (polyomino, (_, polyomino_properties)) in enumerate(
            zip(self.polyominos, self.polyomino_mapping.items())
        ):
            if (
                "rotation_correction" in polyomino_properties
                and polyomino_properties.rotation_correction != 0
            ):
                rotated_polyomino = [
                    [
                        -y * polyomino_properties.rotation_correction,
                        x * polyomino_properties.rotation_correction,
                    ]
                    for [x, y] in polyomino
                ]

                self.polyominos[i] = rotated_polyomino
                updated_polyomino_mapping[
                    tuple(tuple(block) for block in rotated_polyomino)
                ] = polyomino_properties
            else:
                updated_polyomino_mapping[
                    tuple(tuple(block) for block in polyomino)
                ] = polyomino_properties

        self.polyomino_mapping = updated_polyomino_mapping

        self._sort()

    def _shift(
        self,
    ) -> None:
        """ """
        updated_polyomino_mapping = {}

        for i, (polyomino, (_, polyomino_properties)) in enumerate(
            zip(self.polyominos, self.polyomino_mapping.items())
        ):
            if "position_correction" in polyomino_properties and any(
                x != 0 for x in polyomino_properties.position_correction
            ):
                shifted_polyomino = [
                    [
                        x + polyomino_properties.position_correction[0],
                        y + polyomino_properties.position_correction[1],
                    ]
                    for [x, y] in polyomino
                ]

                self.polyominos[i] = shifted_polyomino
                updated_polyomino_mapping[
                    tuple(tuple(block) for block in shifted_polyomino)
                ] = polyomino_properties
            else:
                updated_polyomino_mapping[
                    tuple(tuple(block) for block in polyomino)
                ] = polyomino_properties

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

        for i, (polyomino, (_, polyomino_properties)) in enumerate(
            zip(self.polyominos, self.polyomino_mapping.items())
        ):
            mirrored_polyomino = [[x, -y] for [x, y] in polyomino]

            self.polyominos[i] = mirrored_polyomino
            updated_polyomino_mapping[
                tuple(tuple(block) for block in mirrored_polyomino)
            ] = polyomino_properties

        self.polyomino_mapping = updated_polyomino_mapping

        self._sort()

    def execute(self):
        """ """
        if self.polyomino_size == 4:
            self._rotate()
            self._shift()
            self._mirror_horizontally()

            return self.polyominos, self.polyomino_mapping

        else:
            return self.polyominos
