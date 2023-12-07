import sys
from collections import Counter
from pathlib import Path

HandType = tuple[int, int, int, int, int]


def kind_to_int(kind: str) -> int:
    mapper = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}

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


def hand_type(hand: HandType) -> int:
    if len(hand) != 5:
        raise ValueError("Invalid hand")

    counts = Counter(hand).most_common()

    number_of_most_common = counts[0][1]
    number_of_unique_cards = len(counts)

    if number_of_unique_cards == 1:
        # five of a kind
        return 6
    elif number_of_unique_cards == 2:
        if number_of_most_common == 4:
            # four of a kind
            return 5
        elif number_of_most_common == 3:
            # full house
            return 4
        else:
            raise ValueError("Invalid hand")
    elif number_of_unique_cards == 3:
        if number_of_most_common == 3:
            # three of a kind
            return 3
        elif number_of_most_common == 2:
            # two pairs
            return 2
        else:
            raise ValueError("Invalid hand")
    elif number_of_unique_cards == 4:
        # one pair
        return 1
    elif number_of_unique_cards == 5:
        # high card
        return 0

    raise ValueError("Invalid hand")


def replace_jocker_with_value(hand: HandType, value: int) -> HandType:
    return tuple(value if card == 1 else card for card in hand)


def best_hand_type(hand: HandType) -> int:
    if len(hand) != 5:
        raise ValueError("Invalid hand")

    valid_values = set(range(2, 15)) - {1}

    return max(
        hand_type(replace_jocker_with_value(hand, value)) for value in valid_values
    )


def key(hand: HandType) -> tuple[int, HandType]:
    return (best_hand_type(hand), hand)


def main(fname: str) -> None:
    data = Path(fname).read_text()

    bets = sorted(parse(data), key=lambda x: key(x[0]))

    print(sum(i * bid for i, (_, bid) in enumerate(bets, start=1)))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
