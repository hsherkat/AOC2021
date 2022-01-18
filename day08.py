from utils import read_input


def distinguishable(display):
    return len(set(display)) in (2, 3, 4, 7)


def part1(notes):
    return sum(sum(1 for word in note[1] if distinguishable(word)) for note in notes)


#############


letters_contained = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}


def num_from_letters(letters):
    out = [num for num, s in letters_contained.items() if s == letters]
    return out[0]


letter_fingerprints = {
    c: sorted([len(s) for s in letters_contained.values() if c in s])
    for c in set("abcdefg")
}


def decoding(note):
    encoded_fingerprints = {
        c: sorted([len(word) for word in note[0] if c in word]) for c in set("abcdefg")
    }
    decoding = {
        encoding: letter
        for encoding, coded_print in encoded_fingerprints.items()
        for letter, fingerprint in letter_fingerprints.items()
        if coded_print == fingerprint
    }
    return decoding


def decode(note):
    decoder = decoding(note)
    nums = [num_from_letters(set([decoder[c] for c in word])) for word in note[1]]
    return int("".join(map(str, nums)))


def part2(notes):
    return sum(decode(note) for note in notes)


#################


def prepare_input():
    input_ = read_input("08")
    lines = [line for line in input_.strip().split("\n")]
    parsed = [[part.split() for part in line.split("|")] for line in lines]
    return parsed


def main():
    notes = prepare_input()
    print(part1(notes))
    print(part2(notes))


if __name__ == "__main__":
    main()

