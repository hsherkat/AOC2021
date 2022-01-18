# pylint: disable=F0401

from dataclasses import dataclass
from itertools import product

from utils import read_input

Char = str


@dataclass
class Trench:
    grid: list[list[Char]]

    def __getitem__(self, idx):
        return self.grid[idx]

    def __str__(self):
        return "\n".join("".join(row) for row in self)

    @property
    def M(self):
        return len(self.grid)

    @property
    def N(self):
        return len(self[0])

    def transpose(self) -> "Trench":
        d = {".": ".", "v": ">", ">": "v"}
        new_grid = [[d[c] for c in row] for row in self]
        return Trench([list(row) for row in zip(*new_grid)])

    def move_right(self) -> "Trench":
        new_grid = []
        for row in self:
            new_row = row[:]
            for i in range(self.N):
                if row[i] == ">" and row[(i + 1) % self.N] == ".":
                    new_row[i] = "."
                    new_row[(i + 1) % self.N] = ">"
            new_grid.append(new_row)
        return Trench(new_grid)

    def update(self) -> "Trench":
        return self.move_right().transpose().move_right().transpose()


def part1(trench: Trench):
    count = 0
    while trench != (updated := trench.update()):
        count += 1
        trench = updated
    return count + 1


def prepare_input():
    input_ = read_input("25").strip().split("\n")
    return Trench([list(line) for line in input_])


def main():
    trench = prepare_input()
    print(part1(trench))


if __name__ == "__main__":
    main()
