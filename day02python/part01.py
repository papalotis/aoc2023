import re
import sys
from pathlib import Path


def parse_line(line: str) -> tuple[int, list[tuple[str, str]]]:
    # example line "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"

    # the game index is extracted from the Game 1: part
    game_index = int(re.search(r"Game (\d+):", line).group(1))

    # the pairs of the form (count, color) are extracted
    pairs = re.findall(r"(\d+) (\w+)", line)

    return game_index, pairs


def extract_greatest_appearance_for_each_color_in_a_game(
    pairs: list[tuple[str, str]]
) -> dict[str, int]:
    greatest_count_for_color = {color: 0 for _, color in pairs}

    for count, color in pairs:
        greatest_count_for_color[color] = max(
            greatest_count_for_color[color], int(count)
        )

    return greatest_count_for_color


def handle_line(line: str) -> int:
    index, pairs = parse_line(line)

    greatest_count_for_color = extract_greatest_appearance_for_each_color_in_a_game(
        pairs
    )

    return (
        greatest_count_for_color["red"] <= 12
        and greatest_count_for_color["green"] <= 13
        and greatest_count_for_color["blue"] <= 14
    ) * index


def main(fname: str) -> None:
    data = Path(fname).read_text()

    print(sum(map(handle_line, data.splitlines())))


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
