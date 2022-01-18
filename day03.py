import collections
from typing import List

from utils import read_input


def flip(c: str) -> str:
    return "1" if c == "0" else "0"


def match_digit(digits: List[str], more_common: bool) -> str:
    zeroes, ones = digits.count("0"), digits.count("1")
    if zeroes == ones:
        return str(int(more_common))
    if more_common:
        return "0" if zeroes > ones else "1"
    else:
        return "1" if zeroes > ones else "0"


def filter_down(seqs: List[str], more_common: bool) -> str:
    candidates = seqs[:]
    for idx in range(len(seqs[0])):
        digits = [seq[idx] for seq in candidates]
        candidates = [
            seq for seq in candidates if seq[idx] == match_digit(digits, more_common)
        ]
        if len(candidates) == 1:
            return candidates[0]

    raise ValueError


def part1(cleaned: List[str]) -> int:
    most_common = "".join(
        "1" if digits.count("1") > digits.count("0") else "0"
        for digits in zip(*cleaned)
    )
    least_common = "".join(flip(c) for c in most_common)
    return int(most_common, 2) * int(least_common, 2)


def part2(cleaned: List[str]) -> int:
    big = filter_down(cleaned, True)
    small = filter_down(cleaned, False)
    return int(big, 2) * int(small, 2)


def main():
    input_ = read_input("03")
    cleaned = input_.strip().split("\n")

    print(part1(cleaned))
    print(part2(cleaned))


if __name__ == "__main__":
    main()
