from dataclasses import dataclass
from itertools import product

from utils import read_input


@dataclass
class Octopi:
    grid: list[list[int]]

    @property
    def M(self):
        return len(self.grid)

    @property
    def N(self):
        return len(self.grid[0])

    @property
    def flashed_idx(self):
        return [
            (i, j)
            for i, j in product(range(self.M), range(self.N))
            if self.grid[i][j] > 9
        ]

    def neighbors_idx(self, i, j):
        return [
            (i + dx, j + dy)
            for dx, dy in product((-1, 0, 1), repeat=2)
            if 0 <= i + dx < self.M and 0 <= j + dy < self.N and (dx, dy) != (0, 0)
        ]

    def neighbors(self, i, j):
        return [self.grid[nx][ny] for nx, ny in self.neighbors_idx(i, j)]

    def update(self):
        for i, j in product(range(self.M), range(self.N)):
            self.grid[i][j] += 1

        seen = set()
        flashed_before = set(self.flashed_idx)
        stack = self.flashed_idx[:]
        while stack:
            i, j = loc = stack.pop()
            if loc in seen:
                continue
            else:
                seen.add(loc)
            for nx, ny in self.neighbors_idx(*loc):
                self.grid[nx][ny] += 1
                if self.grid[nx][ny] > 9 and (nx, ny) not in flashed_before:
                    stack.append((nx, ny))

        flash_count = len(self.flashed_idx)
        for i, j in self.flashed_idx:
            self.grid[i][j] = 0

        return flash_count


def part1(octopi):
    return sum(octopi.update() for _ in range(100))


def part2(octopi):
    step = 0
    while (total := sum(sum(row) for row in octopi.grid)) != 0:
        step += 1
        octopi.update()
    return step


def prepare_input():
    return [[int(c) for c in line] for line in read_input("11").strip().split("\n")]


def main():
    octopi = Octopi(prepare_input())
    print(part1(octopi))
    octopi = Octopi(prepare_input())
    print(part2(octopi))


if __name__ == "__main__":
    main()
