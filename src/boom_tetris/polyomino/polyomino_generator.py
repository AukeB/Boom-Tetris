""" """

from src.boom_tetris.constants import Block


class PolyominoGenerator:
    """ """

    def __init__(self, number_of_polyomino_cells: int, directions: list) -> None:
        """ """
        self.number_of_polyomino_cells = number_of_polyomino_cells
        self.directions = directions
        self.unique_coordinates = set()
        self.unique_polyominos = []

    def _normalize(
        self,
        coordinates: set[tuple[int, int]],
    ) -> set[tuple[int, int]]:
        """ """
        x_min = min(x for x, _ in coordinates)
        y_min = min(y for _, y in coordinates)

        normalized_coordinates = tuple(
            sorted((x - x_min, y - y_min) for x, y in coordinates)
        )

        return normalized_coordinates

    def _rotate(self, coordinates: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """ """
        rotated_coordinates = set((y, -x) for x, y in coordinates)

        return rotated_coordinates

    def _obtain_all_rotations(
        self, coordinates: set[tuple[int, int]]
    ) -> list[set[tuple[int, int]]]:
        """ """
        rotations = []

        for _ in len(self.directions):
            coordinates = self._rotate(coordinates)
            coordinates = self._normalize(coordinates)
            rotations.append(coordinates)

        return rotations

    def _register_unique_polyomino(self, normalized_coordinates: set[tuple[int, int]]):
        """ """
        self.unique_coordinates.add(normalized_coordinates)

        polyomino = [
            Block(coordinate[0], coordinate[1]) for coordinate in normalized_coordinates
        ]

        self.unique_polyominos.append(polyomino)

    def generate(self, coordinates: set[tuple[int, int]] = {(0, 0)}) -> set:
        """ """
        number_of_cells = len(coordinates)

        if number_of_cells == self.number_of_polyomino_cells:
            normalized_coordinates = self._normalize(coordinates=coordinates)
            rotation_invariant_coordinates = self._obtain_all_rotations(
                coordinates=normalized_coordinates
            )

            if any(
                coordinates in self.unique_coordinates
                for coordinates in rotation_invariant_coordinates
            ):
                return

            self._register_unique_polyomino(normalized_coordinates)

        for x, y in list(coordinates):
            for _, (dx, dy) in self.directions.items():
                nx, ny = x + dx, y + dy

                if (nx, ny) in coordinates:
                    continue

                new_coordinates = coordinates | {(nx, ny)}

                if number_of_cells <= self.number_of_polyomino_cells:
                    self.generate(coordinates=new_coordinates)

        return self.unique_coordinates
