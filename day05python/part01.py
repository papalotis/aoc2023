import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Self


class Map(Mapping[int, int]):
    def __init__(self, ranges: list[tuple[int, int, int]]) -> None:
        self.source_ranges = []
        self.destination_ranges = []

        for destination_start, source_start, length in ranges:
            destinations_range = range(destination_start, destination_start + length)
            sources_range = range(source_start, source_start + length)

            self.source_ranges.append(sources_range)
            self.destination_ranges.append(destinations_range)

    @classmethod
    def from_string(cls, string: str) -> Self:
        lines = string.splitlines()
        ranges = [tuple(map(int, line.split())) for line in lines[1:]]

        return cls(ranges)

    def __getitem__(self, key: int) -> int:
        for source_range, destination_range in zip(
            self.source_ranges, self.destination_ranges
        ):
            if key in source_range:
                return destination_range[key - source_range.start]

        return key

    def __iter__(self):
        raise NotImplementedError("This mapping does not support iteration")

    def __len__(self):
        raise NotImplementedError("This mapping does not support len")


@dataclass
class Solution:
    maps: list[Map]
    seeds_to_do: list[int]

    @classmethod
    def from_string(cls, string: str) -> Self:
        parts = string.split("\n\n")

        seeds = [int(x) for x in parts[0].split(":")[1].split()]

        maps = [Map.from_string(x) for x in parts[1:]]

        return cls(maps, seeds)

    def do_one_seed(self, seed: int) -> int:
        assert seed in self.seeds_to_do

        value = seed

        for m in self.maps:
            value = m[value]

        return value

    def do_all_seeds(self) -> list[int]:
        return [self.do_one_seed(seed) for seed in self.seeds_to_do]


def main(fname: str) -> None:
    data = Path(fname).read_text()

    solution = Solution.from_string(data)

    locations = solution.do_all_seeds()

    print(min(locations))


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
