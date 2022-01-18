# pylint: disable=F0401

from dataclasses import dataclass
from functools import reduce
from itertools import chain, combinations, islice, tee
from typing import Iterator, Optional, Union

from utils import read_input


@dataclass
class SnailNode:
    val: Optional[int] = None
    left: Optional["SnailNode"] = None
    right: Optional["SnailNode"] = None
    depth: int = 0

    def __repr__(self) -> str:
        return (
            f"{self.val}"
            if self.val is not None
            else f"[{self.left!r}, {self.right!r}]"
        )

    @property
    def is_num(self) -> bool:
        return self.val is not None

    @property
    def is_num_pair(self) -> bool:
        if not self.is_num:
            return self.left.is_num and self.right.is_num
        return False

    def in_order_nums(self) -> Iterator["SnailNode"]:
        if self.left is not None:
            yield from self.left.in_order_nums()
        if self.is_num:
            yield self
        if self.right is not None:
            yield from self.right.in_order_nums()

    def in_order_pairs(self) -> Iterator["SnailNode"]:
        if self.left is not None:
            yield from self.left.in_order_pairs()
        if self.is_num_pair:
            yield self
        if self.right is not None:
            yield from self.right.in_order_pairs()

    def predecessor(self, num: "SnailNode") -> Optional["SnailNode"]:
        if not num.is_num:
            raise ValueError
        it1, it2 = tee(self.in_order_nums(), 2)
        it2 = islice(it2, 1, None)
        for (pred, node) in zip(it1, it2):
            if node is num:
                return pred
        return None

    def successor(self, num: "SnailNode") -> Optional["SnailNode"]:
        if not num.is_num:
            raise ValueError
        it1, it2 = tee(self.in_order_nums(), 2)
        it2 = islice(it2, 1, None)
        for (node, succ) in zip(it1, it2):
            if node is num:
                return succ
        return None

    def explode(self, pair: "SnailNode"):
        L, R = pair.left, pair.right
        if L and L.is_num and R and R.is_num:
            pred = self.predecessor(L)
            succ = self.successor(R)
        else:
            raise ValueError(f"{pair} is not a numeric pair.")
        if pred is not None:
            if pred.is_num:
                pred.val += L.val
            else:
                raise ValueError(f"{pred} is not a numeric node.")
        if succ is not None:
            if succ.is_num:
                succ.val += R.val
            else:
                raise ValueError(f"{succ} is not a numeric node.")
        pair.val = 0
        pair.left = None
        pair.right = None
        return

    def split(self, num: "SnailNode"):
        if num.is_num:
            n = num.val
        else:
            raise ValueError(f"{num} is not a numeric node.")
        num.val = None
        num.left = SnailNode(val=(n // 2), depth=num.depth + 1)
        num.right = SnailNode(val=(n + 1) // 2, depth=num.depth + 1)
        return

    def reduce(self):
        explode_pairs = filter(lambda p: p.depth >= 4, self.in_order_pairs())
        split_nums = filter(lambda n: n.val >= 10, self.in_order_nums())
        node_to_process = next(chain(explode_pairs, split_nums), None)
        if node_to_process is None:
            return
        if node_to_process.is_num_pair:
            self.explode(node_to_process)
        else:
            self.split(node_to_process)
        self.reduce()

    def magnitude(self) -> int:
        if self.is_num:
            return self.val
        else:
            return (3 * self.left.magnitude()) + (2 * self.right.magnitude())

    def __add__(self, other):
        expr_str = f"[{self!r}, {other!r}]"
        sum_ = SnailNode.parse(eval(expr_str))
        sum_.reduce()
        return sum_

    def __eq__(self, other):
        return repr(self) == repr(other)

    @staticmethod
    def parse(
        expr: Union[list, int], parent: Optional["SnailNode"] = None
    ) -> "SnailNode":
        if isinstance(expr, list):
            expr_left, expr_right = expr
            node = SnailNode(depth=parent.depth + 1 if parent else 0)
            left, right = (
                SnailNode.parse(expr_left, parent=node),
                SnailNode.parse(expr_right, parent=node),
            )
            node.left = left
            node.right = right
            return node
        elif isinstance(expr, int):
            return SnailNode(val=expr, depth=parent.depth + 1 if parent else 0)
        else:
            raise ValueError


def part1(snail_nums: list[SnailNode]):
    total = reduce(lambda x, y: x + y, snail_nums)
    return total.magnitude()


def part2(snail_nums: list[SnailNode]):
    snail_num_pairs = combinations(snail_nums, 2)
    magnitudes_of_sums = (
        [(x + y).magnitude(), (y + x).magnitude()] for x, y in snail_num_pairs
    )
    return max(chain.from_iterable(magnitudes_of_sums))


def prepare_input():
    input_ = read_input("18").strip().split("\n")
    return [SnailNode.parse(eval(line)) for line in input_]


def main():
    snail_nums = prepare_input()
    print(part1(snail_nums))
    print(part2(snail_nums))


if __name__ == "__main__":
    main()
