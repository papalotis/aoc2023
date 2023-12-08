import sys
from itertools import cycle
from pathlib import Path


def parse_graph_line(line: str) -> tuple[str, dict[str, str]]:
    source, left_right = line.split(" = ")

    left_with_brackets, right_with_brackets = left_right.split(",")

    left = "".join(filter(str.isalpha, left_with_brackets))
    right = "".join(filter(str.isalpha, right_with_brackets))

    return source, {"L": left, "R": right}


def parse(data: str) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions, graph_str = data.split("\n\n")

    graph = dict(map(parse_graph_line, graph_str.splitlines()))

    return instructions, graph


def solve(instructions: str, graph: dict[str, tuple[str, str]]) -> int:
    current_node = "AAA"

    for i, instruction in enumerate(cycle(instructions)):
        if current_node == "ZZZ":
            return i

        current_node = graph[current_node][instruction]


def main(fname: str) -> None:
    data = Path(fname).read_text()

    instructions, graph = parse(data)

    print(solve(instructions, graph))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).with_name("example_data.txt"))
    main(fname)
