import itertools as it
from typing import List

from utils import read_input


def nwise(itr, n):
    copies = it.tee(itr, n)
    return zip(*[it.islice(copy, i, None) for i, copy in enumerate(copies)])


def part1(cleaned: List[int]) -> int:
    it1, it2 = it.tee(cleaned, 2)
    it2 = it.islice(it2, 1, None)
    return sum(a < b for a, b in zip(it1, it2))


def part2(cleaned: List[int]) -> int:
    window_sums = [sum(triple) for triple in nwise(cleaned, 3)]
    return part1(window_sums)


def main():
    input_ = read_input("01")

    cleaned = [int(line) for line in input_.strip().split("\n")]
    print(part1(cleaned))
    print(part2(cleaned))


if __name__ == "__main__":
    main()
