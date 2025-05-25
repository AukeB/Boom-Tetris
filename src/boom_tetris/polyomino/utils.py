""" """

from src.boom_tetris.constants import Block


def convert_all_polyominos_to_block_objects(
    all_coordinates: list[list[list[int, int]]],
) -> list[list[Block]]:
    """ """
    all_polyominos = []

    for coordinates in all_coordinates:
        polyomino = [Block(y, x) for y, x in coordinates]
        all_polyominos.append(polyomino)

    return all_polyominos
