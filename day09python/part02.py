import sys
from pathlib import Path

import numpy as np

IntArray = np.ndarray[int]


def parse_line(line: str) -> IntArray:
    return np.array([int(x) for x in line.split()])


def parse(data: str) -> list[IntArray]:
    return [parse_line(line) for line in data.splitlines()]


def solve_one(data: IntArray) -> int:
    values = []
    while np.any(data != 0):
        values.append(data[0])
        data = np.diff(data)

    result = 0
    for value in values[::-1]:
        result = value - result

    return result


def solve(data: list[IntArray]) -> int:
    return sum(solve_one(line) for line in data)


def main(fname: str) -> None:
    data = Path(fname).read_text()

    print(solve(parse(data)))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).with_name("example_data.txt"))
    main(fname)
