from collections import Counter

from utils import read_input


def update_timer_counts(counts):
    zeros = counts[0]
    new_counts = Counter(
        {time - 1: count for time, count in counts.items() if time != 0}
    )
    new_counts[8] = zeros
    new_counts[6] += zeros
    return new_counts


def prepare_input():
    input_ = read_input("06")
    timers_str = input_.strip().split(",")
    timers = map(int, timers_str)
    return list(timers)


def part1(timers):
    counts = Counter(timers)
    for _ in range(80):
        counts = update_timer_counts(counts)
    return sum(counts.values())


def part2(timers):
    counts = Counter(timers)
    for _ in range(256):
        counts = update_timer_counts(counts)
    return sum(counts.values())


def main():
    timers = prepare_input()
    print(part1(timers))
    print(part2(timers))


if __name__ == "__main__":
    main()
