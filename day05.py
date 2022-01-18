import re
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import NamedTuple

from utils import read_input


class Point(NamedTuple):
    x: int
    y: int


P = Point  # less clutter


@dataclass(frozen=True, eq=True)
class Segment:
    p1: Point
    p2: Point

    @property
    def is_hori(self):
        return self.p1.y == self.p2.y

    @property
    def is_vert(self):
        return self.p1.x == self.p2.x

    @property
    def lattice_points(self):
        if self.is_vert:
            lo, hi = sorted([self.p1.y, self.p2.y])
            return [P(self.p1.x, y) for y in range(lo, hi + 1)]

        elif self.is_hori:
            L, R = sorted([self.p1.x, self.p2.x])
            return [P(x, self.p1.y) for x in range(L, R + 1)]

        else:
            sgn = 1 if self.p2.y > self.p1.y else -1
            L, R = sorted([self.p1.x, self.p2.x])
            return [P(self.p1.x + i, self.p1.y + (i * sgn)) for i in range(1 + R - L)]


def lattice_segment_counts(segments: list[Segment], exclude_diagonal=True):
    counts = Counter()
    segs = (
        filter(lambda s: s.is_hori or s.is_vert, segments)
        if exclude_diagonal
        else segments
    )
    for seg in segs:
        for pt in seg.lattice_points:
            counts[pt] += 1
    return counts


def part1(segments: list[Segment]):
    counts = lattice_segment_counts(segments)
    return sum(1 for pt, count in counts.items() if count >= 2)


def part2(segments: list[Segment]):
    counts = lattice_segment_counts(segments, exclude_diagonal=False)
    return sum(1 for pt, count in counts.items() if count >= 2)


def prepare_input():
    input_ = read_input("05")

    pattern = re.compile(
        r"""
    (\d+),(\d+)
    [^\d]+ # arrow
    (\d+),(\d+)
    """,
        re.VERBOSE,
    )

    nums = [
        map(int, re.match(pattern, line).groups())
        for line in input_.strip().split("\n")
    ]
    pairs_of_points = [(P(a, b), P(c, d)) for a, b, c, d in nums]
    segments = [Segment(*sorted(pair)) for pair in pairs_of_points]
    return segments


def main():
    segments = prepare_input()
    print(part1(segments))
    print(part2(segments))


if __name__ == "__main__":
    main()
