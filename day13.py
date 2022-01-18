from dataclasses import dataclass
from operator import itemgetter
from typing import NamedTuple

from utils import read_input


class FoldInstruction(NamedTuple):
    direction: str
    location: int

    @staticmethod
    def parse(line):
        location = int(line.split("=")[-1])
        direction = "x" if "x" in line else "y"
        return FoldInstruction(direction, location)


def reflect(val: int, inflection: int):
    return 2 * inflection - val


@dataclass
class Paper:
    dots: set[tuple[int, int]]

    def fold(self, instr: FoldInstruction):
        if instr.direction == "x":
            return self._x_fold(instr.location)
        if instr.direction == "y":
            return self._y_fold(instr.location)

    def _x_fold(self, location: int):
        new_dots = set()
        for (i, j) in self.dots:
            if i < location:
                new_dots.add((i, j))
            else:
                new_dots.add((reflect(i, location), j))
        return Paper(new_dots)

    def _y_fold(self, location: int):
        new_dots = set()
        for (i, j) in self.dots:
            if j < location:
                new_dots.add((i, j))
            else:
                new_dots.add((i, reflect(j, location)))
        return Paper(new_dots)


def part1(paper: Paper, fold_instructions: list[FoldInstruction]):
    return len(paper.fold(fold_instructions[0]).dots)


def part2(paper: Paper, fold_instructions: list[FoldInstruction]):
    for fold_instr in fold_instructions:
        paper = paper.fold(fold_instr)
    M = max(paper.dots, key=itemgetter(1))[1]
    N = max(paper.dots, key=itemgetter(0))[0]
    grid = [["."] * (M + 1) for _ in range(N + 1)]
    for i, j in paper.dots:
        grid[i][j] = "#"
    return grid


def prepare_input():
    input_ = read_input("13").strip()
    raw_dots, raw_folds = input_.split("\n\n")
    dots = [
        (int(a), int(b))
        for (a, b) in [line.split(",") for line in raw_dots.split("\n")]
    ]
    folds = [FoldInstruction.parse(line) for line in raw_folds.split("\n")]
    return Paper(dots), folds


def main():
    paper, fold_instructions = prepare_input()
    print(part1(paper, fold_instructions))
    for line in zip(*part2(paper, fold_instructions)):
        print("".join(line))


if __name__ == "__main__":
    main()
