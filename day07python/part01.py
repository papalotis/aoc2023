import sys
from collections import Counter
from pathlib import Path

HandType = tuple[int, int, int, int, int]


def kind_to_int(kind: str) -> int:
    mapper = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

    return int(mapper.get(kind, kind))


def parse_single_bet(bet: str) -> tuple[HandType, int]:
    hand_str, bid_str = bet.split()

    hand = tuple(map(kind_to_int, hand_str))
    assert len(hand) == 5

    bid = int(bid_str)

    return hand, bid


def parse(data: str) -> list[tuple[HandType, int]]:
    lines = data.splitlines()

    return list(map(parse_single_bet, lines))


def hand_type_key(hand: HandType) -> tuple[int, list[int], HandType]:
    if len(hand) != 5:
        raise ValueError("Invalid hand")

    counts = Counter(hand).most_common()

    occurrences = sorted((count for _, count in counts), reverse=True)

    # the less unique cards, the better
    # if the number of unique cards is the same, the more occurrences of the most common card, the better
    # finally sort by the hand itself
    return -len(occurrences), occurrences, hand


def main(fname: str) -> None:
    data = Path(fname).read_text()

    bets = sorted(parse(data), key=lambda x: hand_type_key(x[0]))

    print(sum(i * bid for i, (_, bid) in enumerate(bets, start=1)))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
