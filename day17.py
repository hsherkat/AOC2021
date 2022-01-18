import re
from dataclasses import dataclass
from typing import NamedTuple

from utils import read_input


def sgn(num):
    if num == 0:
        return 0
    return 1 if num > 0 else -1


@dataclass
class Position:
    x: int = 0
    y: int = 0


@dataclass
class Velocity:
    x: int
    y: int


class Range(NamedTuple):
    lo: int
    hi: int


class Target(NamedTuple):
    x: Range
    y: Range


@dataclass
class Probe:
    position: Position
    velocity: Velocity

    def step(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.velocity.y -= 1
        self.velocity.x = sgn(self.velocity.x) * abs(self.velocity.x - 1)

    def in_target(self, target):
        return (
            target.x.lo <= self.position.x <= target.x.hi
            and target.y.lo <= self.position.y <= target.y.hi
        )

    def max_height(self, target: Target):
        """Only returns if it actually lands in target; returns None otherwise.
        """
        max_height = self.position.y
        while self.position.x <= target.x.hi and self.position.y > target.y.lo:
            self.step()
            if self.in_target(target):
                return max_height
            else:
                max_height = max(max_height, self.position.y)
        return None


def part1(target: Target):
    v_bound = 159
    probes = [
        Probe(Position(0, 0), Velocity(x, y))
        for x in range(1, v_bound)
        for y in range(1, v_bound)
    ]
    return max(max_y for probe in probes if (max_y := probe.max_height(target)))


def part2(target):
    v_bound = 159
    probes = [
        Probe(Position(0, 0), Velocity(x, y))
        for x in range(1, v_bound)
        for y in range(-v_bound, v_bound)
    ]
    return sum(1 for probe in probes if probe.max_height(target) is not None)


def prepare_input():
    input_ = read_input("17").strip()
    pattern = r"(-?\d+)\.\.(-?\d+)"
    x_target, y_target = re.findall(pattern, input_)
    return Target(Range(*map(int, x_target)), Range(*map(int, y_target)))


def main():
    target = prepare_input()
    print(part1(target))
    print(part2(target))


if __name__ == "__main__":
    main()
