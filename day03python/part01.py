import sys
from itertools import product
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def extract_number_and_special_positions(
    data: str,
) -> tuple[list[list[tuple[int, int]]], list[tuple[int, int]]]:
    lines = data.splitlines()

    numbers_start_end_xys: list[list[tuple[int, int]]] = [[]]

    all_xys = list(product(range(len(lines)), range(len(lines[0]))))

    special_idxs: list[tuple[int, int]] = []

    for i, (y, x) in enumerate(all_xys):
        char = lines[y][x]

        prev_y, prev_x = all_xys[i - 1]

        if char.isdigit():
            numbers_start_end_xys[-1].append((y, x))

        elif not char.isdigit() and lines[prev_y][prev_x].isdigit():
            numbers_start_end_xys.append([])

        if not char.isdigit() and char != ".":
            special_idxs.append((y, x))

    if len(numbers_start_end_xys[-1]) == 0:
        numbers_start_end_xys.pop()
    return numbers_start_end_xys, special_idxs


def numbers_from_xys(data: str, xys: list[list[tuple[int, int]]]) -> list[int]:
    lines = data.splitlines()

    return [int("".join(lines[y][x] for y, x in xy)) for xy in xys]


def main(fname: str) -> None:
    data = Path(fname).read_text()

    numbers_start_end_xys, special_idxs = extract_number_and_special_positions(data)

    mask_numbers = mask_numbers_adjacent_to_special_character(
        numbers_start_end_xys, special_idxs
    )

    numbers = numbers_from_xys(data, numbers_start_end_xys)

    print(np.sum(np.array(numbers)[mask_numbers]))


def mask_numbers_adjacent_to_special_character(
    numbers_start_end_xys: list[list[tuple[int, int]]],
    special_idxs: list[tuple[int, int]],
) -> NDArray[np.bool_]:
    numbers_start_end_xys = [[first, last] for first, *_, last in numbers_start_end_xys]

    numbers_array = np.array(numbers_start_end_xys)
    specials_array = np.array(special_idxs)

    diff = numbers_array - specials_array[:, None, None]

    distances = np.linalg.norm(diff, axis=-1)

    min_last_2 = np.min(distances, axis=(-1,))

    return np.any(min_last_2 < 1.5, axis=0)


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
