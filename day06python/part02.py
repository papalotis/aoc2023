import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def parse_data(data: str) -> NDArray[np.int64]:
    times_str, distances_str = data.splitlines()

    times = int("".join(filter(str.isdigit, times_str)))
    distances = int("".join(filter(str.isdigit, distances_str)))

    return np.array([[times, distances]])


def solve(data_array: NDArray[np.int64]) -> int:
    times = data_array[:, 0]
    max_times = np.max(times)

    time_driving = np.arange(max_times + 1)
    speeds = times[:, np.newaxis] - time_driving

    achieved_distances = time_driving * speeds

    mask_over_record = achieved_distances > data_array[:, [1]]

    n_over_record_for_each_entry = np.sum(mask_over_record, axis=1)

    final_product = np.prod(n_over_record_for_each_entry)

    return final_product


def main(fname: str) -> None:
    data = Path(fname).read_text()

    data_array = parse_data(data)

    print(solve(data_array))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
