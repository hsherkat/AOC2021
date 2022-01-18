# pylint: disable=F0401

from dataclasses import dataclass
from functools import cache
from itertools import cycle, islice, product
from typing import NamedTuple


@dataclass
class GameState:
    scores: dict[int, int]
    positions: dict[int, int]
    turn: int = 1

    @property
    def leader(self):
        return max(self.scores, key=lambda p: self.scores[p])

    @property
    def next_turn(self):
        return 2 if self.turn == 1 else 1


def take(n, it):
    return list(islice(it, 0, n))


move = take


def deterministic_die(n):
    return cycle(range(1, n + 1))


def part1(scores, positions):
    die = deterministic_die(100)
    N_rolls = 0
    while max(scores.values()) < 1000:
        rolls = take(3, die)
        N_rolls += 3
        scores[1] += move(sum(rolls), positions[1])[-1]

        if max(scores) >= 1000:
            break

        rolls = take(3, die)
        N_rolls += 3
        scores[2] += move(sum(rolls), positions[2])[-1]

    return min(scores.values()) * N_rolls


# def part1(scores, positions):
#     game = GameState(scores, positions)
#     die = deterministic_die(100)
#     N_rolls = 0
#     while max(scores.values()) < 1000:
#         rolls = take(3, die)
#         N_rolls += 3
#         game.scores[1] += move(sum(rolls), game.positions[1])[-1]

#         if max(game.scores) >= 1000:
#             break

#         rolls = take(3, die)
#         N_rolls += 3
#         game.scores[2] += move(sum(rolls), game.positions[2])[-1]

#     return min(game.scores.values()) * N_rolls


wins = {1: 0, 2: 0}


class State(NamedTuple):
    scores: tuple[int, int]
    positions: tuple[int, int]
    turn: int  # players are 0 and 1


@cache
def ways_to_reach(state: State, initial_state: State):

    # base cases
    if state == initial_state:
        return 1
    if state.scores < initial_state.scores:
        return 0

    player = prev_turn = 1 - state.turn  # it was the other player's turn
    prev_states = []

    # loop over all possible outcomes of 3 rolls and go back a turn
    for roll_seq in product(range(1, 4), repeat=3):
        roll = sum(roll_seq)
        scores = list(state.scores)
        positions = list(state.positions)

        scores[player] -= positions[player]
        positions[player] -= roll
        positions[player] = (positions[player] - 1) % 10 + 1

        if max(scores) < 21:  # otherwise game already over
            prev_states.append(
                State(scores=tuple(scores), positions=tuple(positions), turn=player)
            )

    return sum(ways_to_reach(prev_state, initial_state) for prev_state in prev_states)


def part2(initial_state: State):
    winning_states_0 = (
        State(scores=(s0, s1), positions=(p0, p1), turn=1)
        for s0 in range(21, 31)
        for s1 in range(1, 21)
        for p0 in range(1, 11)
        for p1 in range(1, 11)
    )
    winning_states_1 = (
        State(scores=(s0, s1), positions=(p0, p1), turn=0)
        for s0 in range(1, 21)
        for s1 in range(21, 31)
        for p0 in range(1, 11)
        for p1 in range(1, 11)
    )
    p0_wins = sum(ways_to_reach(state, initial_state) for state in winning_states_0)
    p1_wins = sum(ways_to_reach(state, initial_state) for state in winning_states_1)
    return max(p0_wins, p1_wins)


def prepare_input():
    scores = {1: 0, 2: 0}
    positions = {1: cycle(range(1, 11)), 2: cycle(range(1, 11))}
    take(2, positions[1])  # hard-coded input
    take(8, positions[2])  # hard-coded input
    return scores, positions


def main():
    scores, positions = prepare_input()
    print(part1(scores, positions))

    # scores = {1: 0, 2: 0}  # hard-coded input
    # positions = {1: 2, 2: 8}  # hard-coded input
    initial_state = State((0, 0), (2, 8), 0)
    print(part2(initial_state))


if __name__ == "__main__":
    main()


###############


# def part2(game: GameState):
#     if max(game.scores.values()) >= 21:
#         wins[game.leader] += 1
#         return

#     player = game.turn
#     other_player = game.next_turn
#     score_copies = [game.scores.copy() for _ in range(3)]

#     new_positions = [game.positions[player] + roll for roll in (1, 2, 3)]
#     for i, x in enumerate(new_positions):
#         if x > 10:
#             new_positions[i] -= 10

#     for score_copy, loc in zip(score_copies, new_positions):
#         score_copy[player] += loc

#     for new_scores, loc in zip(score_copies, new_positions):
#         new_game = GameState(
#             new_scores,
#             positions={player: loc, other_player: game.positions[other_player],},
#             turn=other_player,
#         )
#         part2(new_game)

