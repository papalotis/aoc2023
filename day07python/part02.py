import sys
from collections import Counter
from pathlib import Path

HandType = tuple[int, int, int, int, int]

JOKER_VALUE = 1


def kind_to_int(kind: str) -> int:
    mapper = {"A": 14, "K": 13, "Q": 12, "J": JOKER_VALUE, "T": 10}

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


def hand_key(
    hand: HandType, value_to_replace_jokers_with: int
) -> tuple[int, list[int], HandType]:
    if len(hand) != 5:
        raise ValueError("Invalid hand")

    hand_with_jokers_replaced = replace_joker_with_value(
        hand, value_to_replace_jokers_with
    )

    counts = Counter(hand_with_jokers_replaced).most_common()

    occurrences = sorted((count for _, count in counts), reverse=True)

    # the less unique cards, the better
    # if the number of unique cards is the same, the more occurrences of the most common card, the better
    # finally sort by the hand itself
    return -len(occurrences), occurrences, hand


def replace_joker_with_value(hand: HandType, value: int) -> HandType:
    return tuple(value if card == JOKER_VALUE else card for card in hand)


def best_hand_key(hand: HandType) -> tuple[int, list[int], HandType]:
    if len(hand) != 5:
        raise ValueError("Invalid hand")

    valid_values = set(range(2, 15)) - {JOKER_VALUE}

    return max(hand_key(hand, value) for value in valid_values)


def main(fname: str) -> None:
    data = Path(fname).read_text()

    bets = sorted(parse(data), key=lambda x: best_hand_key(x[0]))

    print(sum(i * bid for i, (_, bid) in enumerate(bets, start=1)))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
