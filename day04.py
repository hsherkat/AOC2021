from collections import Counter
from dataclasses import dataclass
from typing import Set, Tuple

from utils import read_input

board_row = list[int]
bingo_board = list[board_row]


@dataclass
class BingoBoard:
    card: bingo_board

    @property
    def rows(self):
        return [row for row in self.card]

    @property
    def cols(self):
        n = len(self.card[0])
        return [[row[i] for row in self.card] for i in range(n)]

    def is_winning(self, draws: Set[int]) -> bool:
        return any(set(row) <= draws for row in self.rows) or any(
            set(col) <= draws for col in self.cols
        )

    @classmethod
    def from_str(cls, raw_rows: str):
        str_rows = raw_rows.split("\n")
        int_rows = [[int(num_str) for num_str in row.split()] for row in str_rows]
        return cls(int_rows)


def get_first_winner(
    draws: list[int], boards: list[BingoBoard]
) -> Tuple[int, BingoBoard]:
    drawn_set = set()
    for num in draws:
        drawn_set.add(num)
        if winners := [board for board in boards if board.is_winning(drawn_set)]:
            return num, winners[0]
    raise ValueError


def get_winners_by_stage(
    draws: list[int], boards: list[BingoBoard]
) -> dict[int, list[BingoBoard]]:

    winners_by_stage: dict[int, list[BingoBoard]] = {}
    drawn_set = set()

    for stage, num in enumerate(draws):
        drawn_set.add(num)
        winners = [board for board in boards if board.is_winning(drawn_set)]
        if len(winners) > len(
            winners_by_stage.get(max(winners_by_stage, default=0), [])
        ):
            winners_by_stage[stage] = winners

    return winners_by_stage


def part1(draws: list[int], boards: list[BingoBoard]):
    stage, winner = get_first_winner(draws, boards)
    drawn_set = set(draws[: stage + 1])
    unmarked_sum = sum(sum(n for n in row if n not in drawn_set) for row in winner.rows)
    return stage * unmarked_sum


def part2(draws: list[int], boards: list[BingoBoard]):
    winners_by_stage = get_winners_by_stage(draws, boards)
    penultimate_stage, last_stage = sorted(winners_by_stage)[-2:]

    last_board = [
        board
        for board in winners_by_stage[last_stage]
        if board not in winners_by_stage[penultimate_stage]
    ][0]

    drawn_set = set(draws[: last_stage + 1])
    unmarked_sum = sum(
        sum(n for n in row if n not in drawn_set) for row in last_board.rows
    )
    return unmarked_sum * draws[last_stage]


def main():
    input_ = read_input("04")
    cleaned = input_.strip().split("\n\n")
    raw_draws, *raw_boards = cleaned
    draws: list[int] = [int(n) for n in raw_draws.split(",")]
    boards: list[BingoBoard] = [BingoBoard.from_str(board) for board in raw_boards]

    print(part1(draws, boards))
    print(part2(draws, boards))


if __name__ == "__main__":
    main()
