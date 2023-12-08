import math
import sys
from itertools import cycle
from pathlib import Path


def parse_graph_line(line: str) -> tuple[str, dict[str, str]]:
    source, left_right = line.split(" = ")

    left_with_brackets, right_with_brackets = left_right.split(",")

    left = "".join(filter(str.isalnum, left_with_brackets))
    right = "".join(filter(str.isalnum, right_with_brackets))

    assert len(source) == 3
    assert len(left) == 3
    assert len(right) == 3

    return source, {"L": left, "R": right}


def parse(data: str) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions, graph_str = data.split("\n\n")

    graph = dict(map(parse_graph_line, graph_str.splitlines()))

    return instructions, graph


def solve_one_node(
    instructions: str, graph: dict[str, tuple[str, str]], start_node: str
) -> int:
    current_node = start_node

    for i, instruction in enumerate(cycle(instructions)):
        if current_node.endswith("Z"):
            return i

        current_node = graph[current_node][instruction]


def solve(instructions: str, graph: dict[str, tuple[str, str]]) -> int:
    cycle_lengths = (
        solve_one_node(instructions, graph, node)
        for node in graph
        if node.endswith("A")
    )

    return math.lcm(*cycle_lengths)


def main(fname: str) -> None:
    data = Path(fname).read_text()
    print(solve(*parse(data)))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).with_name("example_data.txt"))
    main(fname)
