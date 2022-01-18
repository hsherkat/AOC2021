import re
from collections import Counter
from typing import NamedTuple

from utils import read_input

Template = str


class InsertionRule(NamedTuple):
    pair: str
    val: str

    @staticmethod
    def parse(line):
        pair, val = line.split(" -> ")
        return InsertionRule(pair, val)


def process(template: Template, rules: list[InsertionRule]) -> Template:
    insertions = dict()
    for rule in rules:
        c1, c2 = rule.pair
        for idx in [m.start() for m in re.finditer(f"{c1}(?={c2})", template)]:
            insertions[idx] = rule.val
    return "".join(
        [
            c + insertions[idx] if idx in insertions else c
            for idx, c in enumerate(template)
        ]
    )


def pairs(x):
    return Counter(zip(x, x[1:]))


def efficient_process(double_counts, rules: list[InsertionRule]):
    new_counts = Counter(double_counts)
    for rule in rules:
        c1, c2 = rule.pair
        x = rule.val
        for (a, b) in double_counts:
            if (a, b) == (c1, c2):
                new_counts[(a, x)] += double_counts[(a, b)]
                new_counts[(x, b)] += double_counts[(a, b)]
                new_counts[(a, b)] -= double_counts[(a, b)]
    new_counts += Counter()  # remove 0s
    return new_counts


def double_to_single_counts(double_counts, initial_template: Template):
    single_counts = Counter()
    for (a, b) in double_counts:
        single_counts[a] += double_counts[(a, b)]
        single_counts[b] += double_counts[(a, b)]
    single_counts[initial_template[0]] += 1
    single_counts[initial_template[-1]] += 1
    for c in single_counts:
        single_counts[c] //= 2
    return single_counts


######################


def part1(template: Template, rules: list[InsertionRule]):
    for _ in range(10):
        template = process(template, rules)
    counts = Counter(template)
    ranked = counts.most_common()
    return ranked[0][1] - ranked[-1][1]


def part2(template: Template, rules: list[InsertionRule]):
    double_counts = pairs(template)
    for _ in range(40):
        double_counts = efficient_process(double_counts, rules)
    counts = double_to_single_counts(double_counts, template)
    ranked = counts.most_common()
    return ranked[0][1] - ranked[-1][1]


########################


def prepare_input() -> tuple[Template, list[InsertionRule]]:
    input_ = read_input("14")
    template, raw_rules = input_.strip().split("\n\n")
    rules = [InsertionRule.parse(line) for line in raw_rules.split("\n")]
    return template, rules


def main():
    template, rules = prepare_input()
    print(part1(template, rules))
    print(part2(template, rules))


if __name__ == "__main__":
    main()
