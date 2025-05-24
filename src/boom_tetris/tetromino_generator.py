""" """


class TetrominoGenerator:
    """ """

    def __init__(self, number_of_tetromino_cells: int) -> None:
        """ """
        self.number_of_tetromino_cells = number_of_tetromino_cells
        self.directions: list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.unique_coordinates = set()
        self.unique_tetrominos = []

    def _normalize(
        self,
        coordinates: set[tuple[int, int]],
    ) -> set[tuple[int, int]]:
        """ """
        y_min = min(y for y, _ in coordinates)
        x_min = min(x for _, x in coordinates)

        normalized_coordinates = tuple(
            sorted((y - y_min, x - x_min) for y, x in coordinates)
        )

        return normalized_coordinates

    def _rotate(self, coordinates: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """ """
        rotated_coordinates = set((-x, y) for y, x in coordinates)

        return rotated_coordinates

    def _obtain_all_rotations(
        self, coordinates: set[tuple[int, int]]
    ) -> list[set[tuple[int, int]]]:
        """ """
        rotations = []

        for _ in range(4):
            coordinates = self._rotate(coordinates)
            coordinates = self._normalize(coordinates)
            rotations.append(coordinates)

        return rotations

    def _coordinates_to_tetrominos(
        self, coordinates: tuple[tuple[int, int], ...]
    ) -> list[list[int]]:
        """ """
        y_max = max(y for y, _ in coordinates)
        x_max = max(x for _, x in coordinates)

        grid = [[0] * (x_max + 1) for _ in range(y_max + 1)]

        for y, x in coordinates:
            grid[y][x] = 1

        return grid

    def generate(self, coordinates: set[tuple[int, int]] = {(0, 0)}) -> set:
        """ """
        number_of_cells = len(coordinates)

        if number_of_cells == self.number_of_tetromino_cells:
            normalized_coordinates = self._normalize(coordinates=coordinates)
            rotation_invariant_coordinates = self._obtain_all_rotations(
                coordinates=normalized_coordinates
            )

            if any(
                coordinates in self.unique_coordinates
                for coordinates in rotation_invariant_coordinates
            ):
                return

            self.unique_coordinates.add(normalized_coordinates)
            tetromino = self._coordinates_to_tetrominos(
                coordinates=normalized_coordinates
            )
            self.unique_tetrominos.append(tetromino)

        for y, x in list(coordinates):
            for dy, dx in self.directions:
                ny, nx = y + dy, x + dx

                if (ny, nx) in coordinates:
                    continue

                new_coordinates = coordinates | {(ny, nx)}

                if number_of_cells <= self.number_of_tetromino_cells:
                    self.generate(coordinates=new_coordinates)

        return self.unique_tetrominos
