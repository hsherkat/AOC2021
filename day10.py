from functools import reduce

from utils import read_input

openers = ("(", "[", "{", "<")
closers = (")", "]", "}", ">")
illegal_vals = dict(zip(closers, [3, 57, 1197, 25137]))
incomplete_vals = dict(zip(closers, [1, 2, 3, 4]))
match = dict(zip(openers, closers))


def legal_match(a, b):
    return (a, b) in match.items()


def find_illegals(line):
    stack = []
    illegals = []
    for c in line:
        if c in openers:
            stack.append(c)
            continue
        if not legal_match(stack.pop(), c):
            illegals.append(c)
    return illegals


def part1(lines):
    return sum(
        illegal_vals[illegals[0]] if (illegals := find_illegals(line)) else 0
        for line in lines
    )


##############


def incomplete_stack(line):
    stack = []
    illegals = []
    for c in line:
        if c in openers:
            stack.append(c)
            continue
        if not legal_match(stack.pop(), c):
            illegals.append(c)
    if not illegals:
        return stack


def completion_score(line):
    if (stack := incomplete_stack(line)) :
        return reduce(
            lambda so_far, c: incomplete_vals[match[c]] + so_far * 5, reversed(stack), 0
        )


def part2(lines):
    scores = [score for line in lines if (score := completion_score(line))]
    N = len(scores)
    return sorted(scores)[N // 2]


##############


def prepare_input():
    return read_input("10").strip().split("\n")


def main():
    lines = prepare_input()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
