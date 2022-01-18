from dataclasses import dataclass
from typing import List

from utils import read_input


@dataclass
class V:
    hor: int
    dep: int

    def __add__(self, other):
        return V(self.hor + other.hor, self.dep + other.dep)

    def __iter__(self):
        yield self.hor
        yield self.dep


def direction(instruction: List[str]) -> V:
    dir, dist_s = instruction
    dist = int(dist_s)
    if dir == "forward":
        return V(dist, 0)
    if dir == "down":
        return V(0, dist)
    else:
        return V(0, -dist)


def part1(cleaned: List[List[str]]) -> int:
    h, d = sum((direction(instr) for instr in cleaned), V(0, 0))
    return h * d


###########


@dataclass
class V2:
    hor: int
    dep: int
    aim: int

    def __add__(self, other):
        return V(self.hor + other.hor, self.dep + other.dep, self.aim + other.aim)

    def __iter__(self):
        yield self.hor
        yield self.dep
        yield self.aim


def direction2(instruction: List[str], loc: V2) -> V2:
    dir, dist_s = instruction
    dist = int(dist_s)
    if dir == "forward":
        return V2(loc.hor + dist, loc.dep + dist * loc.aim, loc.aim)
    if dir == "down":
        return V2(loc.hor, loc.dep, loc.aim + dist)
    else:
        return V2(loc.hor, loc.dep, loc.aim - dist)


def part2(cleaned: List[List[str]]) -> int:
    loc = V2(0, 0, 0)
    for instr in cleaned:
        loc = direction2(instr, loc)
    return loc.hor * loc.dep


def main():
    input_ = read_input("02")

    cleaned = [line.split() for line in input_.strip().split("\n")]
    print(part1(cleaned))
    print(part2(cleaned))


if __name__ == "__main__":
    main()
