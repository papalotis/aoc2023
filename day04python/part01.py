import sys
from pathlib import Path


def handle_line(line: str) -> int:
    _, values = line.split(":")

    my_values, winning_values = values.split("|")

    my_numbers = map(int, my_values.split())
    winning_numbers = map(int, winning_values.split())

    n_common = len(set(my_numbers).intersection(winning_numbers))

    return int(2 ** (n_common - 1))


def main(fname: str) -> None:
    data = Path(fname).read_text()

    print(sum(map(handle_line, data.splitlines())))


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
