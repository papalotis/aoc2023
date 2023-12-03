from pathlib import Path


def handle_line(line: str):
    mask_is_digit = list(map(str.isdigit, line))

    first_digit_index = mask_is_digit.index(True)
    last_digit_index = len(mask_is_digit) - mask_is_digit[::-1].index(True) - 1

    first_digit = int(line[first_digit_index])
    last_digit = int(line[last_digit_index])

    return first_digit * 10 + last_digit


def main(fname: str) -> None:
    data = Path(fname).read_text()
    print(sum(map(handle_line, data.splitlines())))


if __name__ == "__main__":
    import sys

    fname, *_ = sys.argv[1:]
    main(fname)
