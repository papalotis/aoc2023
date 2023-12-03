import numpy as np
import pytest
from part01 import (
    extract_number_and_special_positions,
    mask_numbers_adjacent_to_special_character,
)


def test_parsing_only_numbers():
    data = """0..1
....
....
2..3"""

    numbers_start_end_xys, special_idxs = extract_number_and_special_positions(data)

    assert numbers_start_end_xys == [[(0, 0)], [(0, 3)], [(3, 0)], [(3, 3)]]

    assert special_idxs == []


def test_parsing_only_specials():
    data = """$..#
....
....
)..$"""

    numbers_start_end_xys, special_idxs = extract_number_and_special_positions(data)

    assert numbers_start_end_xys == []

    assert special_idxs == [(0, 0), (0, 3), (3, 0), (3, 3)]


def test_parsing_with_special():
    data = """0..1
#...
....
2..3"""

    numbers_start_end_xys, special_idxs = extract_number_and_special_positions(data)

    assert numbers_start_end_xys == [
        [(0, 0)],
        [(0, 3)],
        [(3, 0)],
        [(3, 3)],
    ], numbers_start_end_xys

    assert special_idxs == [(1, 0)], special_idxs


def test_parsing_with_example():
    data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    numbers_start_end_xys, special_idxs = extract_number_and_special_positions(data)

    assert numbers_start_end_xys == [
        [(0, 0), (0, 1), (0, 2)],
        [(0, 5), (0, 6), (0, 7)],
        [(2, 2), (2, 3)],
        [(2, 6), (2, 7), (2, 8)],
        [(4, 0), (4, 1), (4, 2)],
        [(5, 7), (5, 8)],
        [(6, 2), (6, 3), (6, 4)],
        [(7, 6), (7, 7), (7, 8)],
        [(9, 1), (9, 2), (9, 3)],
        [(9, 5), (9, 6), (9, 7)],
    ]

    assert special_idxs == [(1, 3), (3, 6), (4, 3), (5, 5), (8, 3), (8, 5)]


def test_filtering1():
    numbers_start_end_xys = [[(0, 0)], [(0, 3)], [(3, 0)], [(3, 3)]]

    special_idxs = [(1, 0)]

    mask = mask_numbers_adjacent_to_special_character(
        numbers_start_end_xys, special_idxs
    )

    np.testing.assert_array_equal(mask, [True, False, False, False])


def test_filtering2():
    numbers_start_end_xys = [[(0, 0)], [(0, 3)], [(3, 0)], [(3, 3)]]

    special_idxs = [(1, 0), (3, 2)]

    mask = mask_numbers_adjacent_to_special_character(
        numbers_start_end_xys, special_idxs
    )

    np.testing.assert_array_equal(mask, [True, False, False, True])


def test_filtering3():
    numbers_start_end_xys = [[(0, 0)], [(0, 3)], [(3, 0)], [(2, 3), (3, 3)]]

    special_idxs = [(1, 0), (1, 3)]

    mask = mask_numbers_adjacent_to_special_character(
        numbers_start_end_xys, special_idxs
    )

    np.testing.assert_array_equal(mask, [True, True, False, True])


def test_filtering_example_data():
    numbers_start_end_xys = [
        [(0, 0), (0, 1), (0, 2)],
        [(0, 5), (0, 6), (0, 7)],
        [(2, 2), (2, 3)],
        [(2, 6), (2, 7), (2, 8)],
        [(4, 0), (4, 1), (4, 2)],
        [(5, 7), (5, 8)],
        [(6, 2), (6, 3), (6, 4)],
        [(7, 6), (7, 7), (7, 8)],
        [(9, 1), (9, 2), (9, 3)],
        [(9, 5), (9, 6), (9, 7)],
    ]

    special_idxs = [(1, 3), (3, 6), (4, 3), (5, 5), (8, 3), (8, 5)]

    mask = mask_numbers_adjacent_to_special_character(
        numbers_start_end_xys, special_idxs
    )

    np.testing.assert_array_equal(
        mask, [True, False, True, True, True, False, True, True, True, True]
    )
