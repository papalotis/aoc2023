import sys
from pathlib import Path


def calc_winnings_for_line(line: str) -> int:
    _, values = line.split(":")

    my_values, winning_values = values.split("|")

    my_numbers = map(int, my_values.split())
    winning_numbers = map(int, winning_values.split())

    n_common = len(set(my_numbers).intersection(winning_numbers))

    return n_common


def main(fname: str) -> None:
    data = Path(fname).read_text()

    lines = data.splitlines()

    cards_to_do = [1 for _ in range(len(lines))]
    cards_done = 0

    for i, line in enumerate(lines):
        winnings = calc_winnings_for_line(line)

        cards_done += cards_to_do[i]

        for j in range(winnings):
            cards_to_do[i + j + 1] += cards_to_do[i]

    print(cards_done)


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
