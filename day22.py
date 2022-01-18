# pylint: disable=F0401

import re
from collections import Counter
from enum import Enum
from itertools import product, starmap
from math import prod
from typing import NamedTuple

from utils import read_input


class Command(Enum):
    """ON or OFF for RebootStep.
    """

    ON = 1
    OFF = -1


class Interval(NamedTuple):
    """Intervals are inclusive on the left, exclusive on the right, just like Python slices.
    This change was made later, so if any problems arise, check to see if this is the cause!
    """

    lo: int
    hi: int

    def __repr__(self) -> str:
        return f"I[{self.lo}, {self.hi})"

    def intersect(self, other: "Interval"):
        """Intersect two intervals.
        """
        left = max(self.lo, other.lo)
        right = min(self.hi, other.hi)
        if left < right:
            return Interval(left, right)
        return None

    def length(self):
        """Number of lattice points in the interval.
        Interval(0,1) is length 1, since only the point 0 is in it -- 
        don't forget exclusive on the right.
        """
        return self.hi - self.lo

    def lattice_points(self):
        return list(range(*self))

    @staticmethod
    def intersection(intervals: list["Interval"]):
        """Intersect a list of intervals.
        """
        out = intervals[0]
        for interval in intervals[1:]:
            out = out.intersect(interval)
            if out is None:
                break
        return out


class Cuboid(NamedTuple):
    x: Interval
    y: Interval
    z: Interval

    def __repr__(self) -> str:
        return f"Cube({', '.join([repr(interval) for interval in self])})"

    def volume(self):
        """Returns number of lattice points in the cuboid.
        Recall intervals are exclusive on the right.
        """
        return prod(map(Interval.length, self))

    def lattice_points(self):
        return list(product(*starmap(range, self)))

    def intersect(self, other: "Cuboid"):
        """Intersect two cuboids.
        """
        intersections = list(map(Interval.intersect, self, other))
        if all(intersections):
            return Cuboid(*intersections)

    @staticmethod
    def intersection(cuboids: list["Cuboid"]):
        """Intersect a list of cuboids.
        """
        out = cuboids[0]
        for cuboid in cuboids[1:]:
            out = out.intersect(cuboid)
            if out is None:
                break
        return out

    @classmethod
    def from_nums(cls, a, b, c, d, e, f):
        i1 = Interval(a, b)
        i2 = Interval(c, d)
        i3 = Interval(e, f)
        return cls(i1, i2, i3)


class RebootStep(NamedTuple):
    cmd: Command
    cuboid: Cuboid

    @staticmethod
    def parse(s: str):
        cmd = Command.ON if s.startswith("on") else Command.OFF

        pattern = re.compile(
            r"""
        \=          # equals sign
        ([^\.]+)    # start of range
        \.\.        # ..
        ([^\.]+)    # end of range
        (?=,|$)     # comma or end of line
        """,
            re.VERBOSE,
        )

        x, y, z = [
            Interval(*([int(lo), int(hi) + 1])) for (lo, hi) in re.findall(pattern, s)
        ]
        return RebootStep(cmd=cmd, cuboid=Cuboid(x, y, z))


def part1(steps: list[RebootStep]):
    cubes = Counter()
    for cmd, new_cube in steps:
        new_counts = Counter()
        for cube, count in cubes.items():
            if (overlap := Cuboid.intersect(cube, new_cube)) is not None:
                new_counts[overlap] -= count
        if cmd == Command.ON:
            new_counts[new_cube] += 1
        cubes.update(new_counts)
    return sum(count * cube.volume() for cube, count in cubes.items())


def prepare_input():
    input_ = read_input("22").strip().split("\n")
    return [RebootStep.parse(line) for line in input_]


def main():
    steps = prepare_input()
    print(part1(steps[:20]))
    print(part1(steps))


if __name__ == "__main__":
    main()
