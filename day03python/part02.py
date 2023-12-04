import sys
from itertools import product
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

IntArray = NDArray[int]


def extract_number_and_special_positions(
    data: str,
) -> tuple[list[list[tuple[int, int]]], list[tuple[int, int]]]:
    lines = data.splitlines()

    numbers_start_end_xys: list[list[tuple[int, int]]] = [[]]

    all_xys = list(product(range(len(lines)), range(len(lines[0]))))

    gear_idxs: list[tuple[int, int]] = []

    for i, (y, x) in enumerate(all_xys):
        char = lines[y][x]

        prev_y, prev_x = all_xys[i - 1]

        if char.isdigit():
            numbers_start_end_xys[-1].append((y, x))

        elif not char.isdigit() and lines[prev_y][prev_x].isdigit():
            numbers_start_end_xys.append([])

        if char == "*":
            gear_idxs.append((y, x))

    if len(numbers_start_end_xys[-1]) == 0:
        numbers_start_end_xys.pop()
    return numbers_start_end_xys, gear_idxs


def numbers_from_xys(data: str, xys: list[list[tuple[int, int]]]) -> list[int]:
    lines = data.splitlines()

    return [int("".join(lines[y][x] for y, x in xy)) for xy in xys]


def calc_indices_of_numbers_adjacent_to_gears(
    numbers_start_end_xys: list[list[tuple[int, int]]],
    gear_idxs: list[tuple[int, int]],
) -> IntArray:
    numbers_start_end_xys = [[first, last] for first, *_, last in numbers_start_end_xys]

    numbers_array = np.array(numbers_start_end_xys)
    specials_array = np.array(gear_idxs)

    diff = numbers_array - specials_array[:, None, None]

    distances = np.linalg.norm(diff, axis=-1)

    mask_keep = np.any(distances < 1.5, axis=-1)
    mask_overwrite = mask_keep.sum(axis=1) < 2
    mask_keep[mask_overwrite] = False
    indices_numbers = np.argwhere(mask_keep)[:, 1].reshape(-1, 2)

    return indices_numbers


def calc_products(
    numbers: list[int], indices_of_numbers_adjacent_to_gears: IntArray
) -> IntArray:
    numbers_array = np.array(numbers)
    selected_numbers = numbers_array[indices_of_numbers_adjacent_to_gears]
    products = np.prod(selected_numbers, axis=1)
    return products


def main(fname: str) -> None:
    data = Path(fname).read_text()

    numbers_start_end_xys, gear_idxs = extract_number_and_special_positions(data)

    indices_of_numbers_adjacent_to_gears = calc_indices_of_numbers_adjacent_to_gears(
        numbers_start_end_xys, gear_idxs
    )

    numbers = numbers_from_xys(data, numbers_start_end_xys)

    products = calc_products(numbers, indices_of_numbers_adjacent_to_gears)

    print(np.sum(products))


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
