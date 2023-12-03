import sys
from pathlib import Path


def create_lookup_table() -> dict[str, int]:
    digit_names = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    string_to_int = {k: v for v, k in enumerate(digit_names)}
    string_to_int |= {k[::-1]: v for k, v in string_to_int.items()}
    string_to_int |= {str(i): i for i in range(10)}

    return string_to_int


STRING_TO_INT = create_lookup_table()


def handle_line(line: str) -> int:
    # cannot use find and min because -1 is returned when not found
    last_digit = max(STRING_TO_INT, key=line.rfind)
    first_digit = max(STRING_TO_INT, key=line[::-1].rfind)

    return STRING_TO_INT[first_digit] * 10 + STRING_TO_INT[last_digit]


def main(fname: str) -> None:
    data = Path(fname).read_text()

    print(sum(map(handle_line, data.splitlines())))


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
