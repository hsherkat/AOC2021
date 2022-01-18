from collections import defaultdict
from dataclasses import dataclass, field
from os import read

from utils import read_input

Vertex = str


@dataclass
class Graph:
    neighbors: dict[Vertex, list[Vertex]]
    vertices: set[Vertex] = field(default_factory=set)
    big_vertices: set[Vertex] = field(default_factory=set)
    small_vertices: set[Vertex] = field(default_factory=set)

    def finish_init(self):
        self.vertices = set(self.neighbors)
        self.big_vertices = set(filter(str.isupper, self.vertices))
        self.small_vertices = set(
            [v for v in filter(str.islower, self.vertices) if v not in ["start", "end"]]
        )

    @classmethod
    def from_edges(cls, edges):
        adjacency_list = defaultdict(list)
        for (a, b) in edges:
            adjacency_list[a].append(b)
            adjacency_list[b].append(a)
        out = cls(dict(adjacency_list))
        out.finish_init()
        return out

    def paths1(self, start: Vertex, end: Vertex):
        """Path may not visit small vertex more than once.
        """
        out = []

        stack: list[tuple[str, ...]] = [(start,)]
        while stack:
            path = stack.pop()
            loc = path[-1]
            for nbr in self.neighbors[loc]:
                if nbr == start:
                    continue
                if nbr == end:
                    out.append(path)
                    continue
                if nbr in self.small_vertices and path.count(nbr) == 1:
                    continue
                stack.append(path + (nbr,))

        return out

    def paths2(self, start: Vertex, end: Vertex):
        """Path may visit a single small vertex twice -- all others at most once.
        """
        out = []

        stack: list[tuple[str, ...]] = [(start,)]
        while stack:
            path = stack.pop()
            loc = path[-1]
            if loc == end:
                out.append(path)
                continue
            for nbr in self.neighbors[loc]:
                if nbr == start:
                    continue
                if nbr in self.small_vertices and nbr in path:
                    if any(path.count(v) == 2 for v in self.small_vertices):
                        continue
                stack.append(path + (nbr,))

        return out


def part1(graph: Graph):
    return len(graph.paths1("start", "end"))


def part2(graph: Graph):
    return len(graph.paths2("start", "end"))


def prepare_input():
    input_ = read_input("12")
    return [edge.split("-") for edge in input_.strip().split("\n")]


def main():
    graph = Graph.from_edges(prepare_input())
    print(part1(graph))
    print(part2(graph))


test_input = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


if __name__ == "__main__":
    main()
