import heapq
from dataclasses import dataclass
from itertools import product

from utils import read_input


@dataclass
class Cavern:
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
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if 0 <= i + dx < self.M and 0 <= j + dy < self.N and (dx, dy) != (0, 0)
        ]

    def neighbors(self, i, j):
        return [self.grid[nx][ny] for nx, ny in self.neighbors_idx(i, j)]


def dijkstra(cavern: Cavern):
    """Distances to (0,0) in cavern"""
    distance_from_origin = {
        (i, j): float("inf") for (i, j) in product(range(cavern.M), range(cavern.N))
    }
    heap = [(dist, loc) for loc, dist in distance_from_origin.items()]
    heapq.heapify(heap)
    distance_from_origin[(0, 0)] = 0
    unseen = set(distance_from_origin)
    while unseen:
        dist_to_loc, loc = heapq.heappop(heap)
        unseen.remove(loc)
        for nbr in cavern.neighbors_idx(*loc):
            x, y = nbr
            new_dist = distance_from_origin[loc] + cavern.grid[x][y]
            if new_dist < distance_from_origin[nbr]:
                distance_from_origin[nbr] = new_dist
                heapq.heappush(heap, (new_dist, nbr))
    return distance_from_origin


def part1(cavern: Cavern):
    distance_from_origin = dijkstra(cavern)
    return distance_from_origin[(cavern.M - 1, cavern.N - 1)]


def part2(cavern: Cavern):
    MM, NN = 5 * cavern.M, 5 * cavern.N
    big_grid = [[0] * NN for _ in range(NN)]
    for (i, j) in product(range(MM), range(NN)):
        div_i, rem_i = divmod(i, cavern.M)
        div_j, rem_j = divmod(j, cavern.N)
        big_grid[i][j] = (
            val
            if (val := (cavern.grid[rem_i][rem_j] + div_i + div_j)) < 10
            else val - 9
        )
    big_cavern = Cavern(big_grid)
    return part1(big_cavern)


##############


def prepare_input():
    input_ = read_input("15")
    grid = [[int(c) for c in row] for row in input_.strip().split("\n")]
    return Cavern(grid)


def main():
    cavern = prepare_input()
    print(part1(cavern))
    print(part2(cavern))


if __name__ == "__main__":
    main()
