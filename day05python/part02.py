from itertools import count
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import NoReturn
from typing_extensions import Self

from tqdm import tqdm


class Map(Mapping[int, int]):
    def __init__(self, ranges: list[tuple[int, int, int]]) -> None:
        source_ranges: list[range] = []
        destination_ranges: list[range] = []

        for destination_start, source_start, length in ranges:
            destinations_range = range(destination_start, destination_start + length)
            sources_range = range(source_start, source_start + length)

            source_ranges.append(sources_range)
            destination_ranges.append(destinations_range)

        self.source_ranges = source_ranges
        self.destination_ranges = destination_ranges

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

    def __iter__(self) -> NoReturn:
        raise NotImplementedError("This mapping does not support iteration")

    def __len__(self) -> NoReturn:
        raise NotImplementedError("This mapping does not support len")
    
class BackwardsMap(Map):
    def __getitem__(self, key: int) -> int:
        for source_range, destination_range in zip(
            self.source_ranges, self.destination_ranges
        ):
            if key in destination_range:
                return source_range[key - destination_range.start]

        return key


@dataclass
class Solution:
    maps: list[Map]
    seeds_ranges: list[range]
    position_and_value_to_result: dict[tuple[int, int], int] = field(
        default_factory=dict, init=False
    )

    @classmethod
    def from_string(cls, string: str) -> Self:
        parts = string.split("\n\n")

        seeds_ints = [int(x) for x in parts[0].split(":")[1].split()]
        seeds = [
            range(start, start + length)
            for start, length in zip(seeds_ints[::2], seeds_ints[1::2])
        ]

        maps = [BackwardsMap.from_string(x) for x in parts[1:][::-1]]

        return cls(maps, seeds)


    def find_best_location(self) -> int:
        found_location = None

        for location in tqdm(count()):
            orig_location = location
            for m in self.maps:
                location = m[location]

            seed = location
            for seed_range in self.seeds_ranges:
                if seed in seed_range:
                    found_location = orig_location
                    
            if found_location is not None:
                break
                    
        return found_location

def main(fname: str) -> None:
    data = Path(fname).read_text()

    solution = Solution.from_string(data)

    location = solution.find_best_location()

    print(location)


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
