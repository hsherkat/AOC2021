import math
from collections import deque
from dataclasses import dataclass
from itertools import product

from utils import read_input


@dataclass
class Caves:
    grid: list[list[int]]

    @property
    def M(self):
        return len(self.grid)

    @property
    def N(self):
        return len(self.grid[0])

    def neighbors_idx(self, i, j):
        return [
            (i + dx, j + dy)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if 0 <= i + dx < self.M and 0 <= j + dy < self.N
        ]

    def neighbors(self, i, j):
        return [self.grid[nx][ny] for nx, ny in self.neighbors_idx(i, j)]

    def is_low_point(self, i, j):
        return all(self.grid[i][j] < neighbor for neighbor in self.neighbors(i, j))

    def basin_size(self, i, j):
        """(i,j) should be a low point!
        """
        q = deque()
        visited = set()
        q.append((i, j))
        while q:
            location = q.popleft()
            x, y = location
            visited.add(location)
            for (nx, ny) in self.neighbors_idx(x, y):
                if (nx, ny) not in visited and self.grid[x][y] < self.grid[nx][ny] < 9:
                    q.append((nx, ny))
        return len(visited)


def part1(caves):
    return sum(
        1 + caves.grid[i][j]
        for i, j in product(range(caves.M), range(caves.N))
        if caves.is_low_point(i, j)
    )


def part2(caves):
    low_points = [
        (i, j)
        for i, j in product(range(caves.M), range(caves.N))
        if caves.is_low_point(i, j)
    ]
    basin_sizes = [caves.basin_size(*low_point) for low_point in low_points]
    return math.prod(sorted(basin_sizes)[-3:])


def prepare_input():
    input_ = read_input("09")
    grid = [[int(c) for c in row] for row in input_.strip().split("\n")]
    return grid


def main():
    caves = Caves(prepare_input())
    print(part1(caves))
    print(part2(caves))


if __name__ == "__main__":
    main()
