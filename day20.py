# pylint: disable=F0401

import numpy as np

from utils import read_input


def pad(image, n, val):
    return np.pad(image, [(n, n), (n, n)], mode="constant", constant_values=val)


def enhance_pixel(i, j, image, algorithm):
    bin_str = "".join(image[i - 1 : i + 2, j - 1 : j + 2].ravel())
    idx = int(bin_str, 2) if bin_str else 0
    return "1" if algorithm[idx] == "#" else "0"


def enhance(image, algorithm, val):
    padded = pad(image, 4, val=val)
    enhanced_img = np.zeros_like(padded)
    for (i, j), pixel in np.ndenumerate(padded):
        enhanced_img[i, j] = enhance_pixel(i, j, padded, algorithm)
    return enhanced_img


def enhance_twice_and_trim(image, algorithm):
    enhanced_once = enhance(image, algorithm, "0")
    enhanced_twice = enhance(enhanced_once, algorithm, enhanced_once[0][0])
    trimmed = enhanced_twice[6:-6, 6:-6]
    return trimmed


def part1(image, algorithm):
    enhanced = enhance_twice_and_trim(image, algorithm)
    return np.count_nonzero(enhanced.astype("int32"))


def part2(image, algorithm):
    for _ in range(25):
        image = enhance_twice_and_trim(image, algorithm)
    return np.count_nonzero(image.astype("int32"))


def prepare_input():
    algorithm, image = read_input("20").strip().split("\n\n")
    # algorithm, image = test_input.strip().split("\n\n")
    algorithm = algorithm.replace("\n", "")
    lines_str = image.strip().split("\n")
    lines_list = [list(s) for s in lines_str]
    arr = np.array(lines_list)
    arr[arr == "."] = 0
    arr[arr == "#"] = 1
    return algorithm, arr


def main():
    algorithm, image = prepare_input()
    print(part1(image, algorithm))
    print(part2(image, algorithm))


test_input = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


if __name__ == "__main__":
    main()

