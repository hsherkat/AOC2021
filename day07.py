from math import ceil, floor

from utils import read_input


def median(nums):
    N = len(nums)
    nums_sorted = sorted(nums)
    return nums_sorted[N // 2] if N % 2 == 1 else nums_sorted[N // 2 - 1]


def mean(nums):
    return sum(nums) / len(nums)


def triag(n):
    return n * (n + 1) // 2


def part1(nums):
    med = median(nums)
    return sum(abs(x - med) for x in nums)


def part2(nums):
    avg = mean(nums)
    avg1 = floor(avg)
    avg2 = ceil(avg)
    return min(
        sum(triag(abs(x - avg1)) for x in nums), sum(triag(abs(x - avg2)) for x in nums)
    )


def prepare_input():
    input_ = read_input("07")
    nums = [int(s) for s in input_.strip().split(",")]
    return nums


def main():
    nums = prepare_input()
    print(part1(nums))
    print(part2(nums))


if __name__ == "__main__":
    main()
