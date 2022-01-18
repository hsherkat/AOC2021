from collections import deque
from dataclasses import dataclass
from itertools import chain, product
from typing import ClassVar, NamedTuple

Amphipod = str


class Point(NamedTuple):
    """A lattice point in the plane."""

    x: int
    y: int

    def __add__(self, other):
        dx, dy = other
        return Point(self.x + dx, self.y + dy)

    @staticmethod
    def dist(pt1, pt2):
        """Manhatten metric between two points, taking into account how they travel in burow.
        """
        return pt1.y + pt2.y + abs(pt1.x - pt2.x)


@dataclass
class BurrowState:
    locations: dict[Amphipod, Point]
    move_counts: dict[Amphipod, int]
    total_cost: int
    burrow: ClassVar[set[Point]]
    room_entrances: ClassVar[set[Point]]
    room_depth: ClassVar[int]
    move_costs: ClassVar[dict[Amphipod, int]]

    @staticmethod
    def destination(amphipod: Amphipod):
        return dict(zip("ABCD", [2, 4, 6, 8]))[amphipod[0]]

    def reachable(self, pt: Point) -> set[Point]:
        left = max(
            [p.x for p in self.locations.values() if p.x < pt.x and p.y == 0],
            default=-1,
        )
        right = min(
            [p.x for p in self.locations.values() if p.x > pt.x and p.y == 0],
            default=11,
        )
        if pt.y == 0:
            out = {Point(x, 0) for x in range(left + 1, right)}
            for entrance in out.intersection(self.room_entrances):
                y = min(
                    [p.y for p in self.locations.values() if p.x == entrance.x],
                    default=self.room_depth + 1,
                )
                out.update({Point(entrance.x, yy) for yy in range(1, y)})
        if pt.y > 0:
            y = max(
                [p.y for p in self.locations.values() if p.x == pt.x and p.y < pt.y],
                default=0,
            )
            if y == 0:
                out = {Point(x, 0) for x in range(left + 1, right)}
                for entrance in out.intersection(self.room_entrances):
                    y = min(
                        [p.y for p in self.locations.values() if p.x == entrance.x],
                        default=self.room_depth + 1,
                    )
                    out.update({Point(entrance.x, yy) for yy in range(1, y)})
            else:
                out = set()
        return out

    def legal_moves(self, amphipod: Amphipod) -> list[Point]:
        """Cannot stop at a room entrance or an occupied site.
        Cannot go into a room that isn't your final destination.
        """
        loc = self.locations[amphipod]
        x_room = BurrowState.destination(amphipod)
        out = [
            point
            for point in self.reachable(loc)
            if point not in self.room_entrances
            and point not in self.locations.values()
            and (point.y == 0 or point.x == x_room)
        ]

        return out

    def possible_states(self) -> list["BurrowState"]:
        out = []
        for amphipod, move_count in self.move_counts.items():
            loc = self.locations[amphipod]
            if move_count >= 2:
                continue
            if move_count == 1:
                x_room = BurrowState.destination(amphipod)
                reachable = self.reachable(loc)
                if (
                    reachable_rooms := (
                        {
                            Point(x_room, y)
                            for y in range(1, BurrowState.room_depth + 1)
                        }.intersection(reachable)
                    )
                ) :
                    destination = max(reachable_rooms)
                    move_cost = self.move_costs[amphipod[0]] * Point.dist(
                        loc, destination
                    )
                    new_locs = dict(self.locations)
                    new_locs[amphipod] = destination
                    new_counts = dict(self.move_counts)
                    new_counts[amphipod] = 2
                    out.append(
                        BurrowState(new_locs, new_counts, self.total_cost + move_cost)
                    )
            if move_count == 0:
                for destination in self.legal_moves(amphipod):
                    move_cost = self.move_costs[amphipod[0]] * Point.dist(
                        loc, destination
                    )
                    new_locs = dict(self.locations)
                    new_locs[amphipod] = destination
                    new_counts = dict(self.move_counts)
                    new_counts[amphipod] = 1
                    out.append(
                        BurrowState(new_locs, new_counts, self.total_cost + move_cost)
                    )
        return out

    @property
    def final(self) -> bool:
        """Is this the final state where every amphipod is in its room?
        """
        y_min = min(pt.y for pt in self.locations.values())
        if y_min == 0:
            return False
        return all(
            loc.x == BurrowState.destination(amphipod)
            for amphipod, loc in self.locations.items()
        )

    def fake_hash(self) -> tuple[Point, ...]:
        """Keeps track of just the arrangement of amphipods.
        Amphipods of same type are interchangeable.
        """
        return tuple(
            chain.from_iterable(
                [
                    sorted(
                        [
                            self.locations[c + str(n)]
                            for n in range(1, BurrowState.room_depth + 1)
                        ]
                    )
                    for c in "ABCD"
                ]
            )
        )


def part1(start_state: BurrowState):
    """BFS to find all possible ways of moving amphipods to their rooms.
    Since the same arrangement can be reached via different moves, keep track of 
    repititions and update the one already in the queue to be optimal.
    """
    best = float("inf")
    q = deque([start_state])
    hash_to_state = {start_state.fake_hash(): start_state}
    while q:
        state = q.popleft()
        if state.final:
            best = min(best, state.total_cost)
            continue
        for new_state in state.possible_states():
            hash_ = new_state.fake_hash()
            if hash_ in hash_to_state:
                prev_state = hash_to_state[hash_]
                if new_state.total_cost < prev_state.total_cost:
                    prev_state.locations = new_state.locations
                    prev_state.move_counts = new_state.move_counts
                    prev_state.total_cost = new_state.total_cost
            else:
                q.append(new_state)
                hash_to_state[hash_] = new_state
    return best


def part2(start_state: BurrowState):
    """Adjusts state for part 2, then calls part 1.
    """
    BurrowState.room_depth = 4
    BurrowState.burrow.update({Point(x, y) for x in (2, 4, 6, 8) for y in (3, 4)})
    amphipods = ["".join(item) for item in product("ABCD", "1234")]
    start_state.move_counts = {amphipod: 0 for amphipod in amphipods}
    new_locations = {
        amphipod: (loc if loc.y == 1 else loc + (0, 2))
        for amphipod, loc in start_state.locations.items()
    }
    new_locations.update(
        {
            "D3": Point(2, 2),
            "D4": Point(2, 3),
            "C3": Point(4, 2),
            "B3": Point(4, 3),
            "B4": Point(6, 2),
            "A3": Point(6, 3),
            "A4": Point(8, 2),
            "C4": Point(8, 3),
        }
    )
    start_state.locations = new_locations
    return part1(start_state)


def prepare_input():
    """Prepares state for part 1.
    """
    burrow = [Point(x, 0) for x in range(11)]
    for x in range(2, 10, 2):
        burrow.extend([Point(x, 1), Point(x, 2)])

    room_entrances = [Point(2, 0), Point(4, 0), Point(6, 0), Point(8, 0)]
    amphipods = ["".join(item) for item in product("ABCD", "12")]
    move_counts = {amphipod: 0 for amphipod in amphipods}
    locations = {
        "A1": Point(2, 1),
        "A2": Point(6, 1),
        "B1": Point(6, 2),
        "B2": Point(8, 2),
        "C1": Point(2, 2),
        "C2": Point(8, 1),
        "D1": Point(4, 1),
        "D2": Point(4, 2),
    }
    move_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    BurrowState.burrow = set(burrow)
    BurrowState.room_entrances = set(room_entrances)
    BurrowState.room_depth = 2
    BurrowState.move_costs = move_costs
    state = BurrowState(locations, move_counts, total_cost=0)
    return state


def main():
    state = prepare_input()
    print(part1(state))
    print(part2(state))


if __name__ == "__main__":
    main()
