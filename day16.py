import itertools as it
from dataclasses import dataclass, field
from math import prod
from typing import Optional

from utils import read_input

HEX_TO_BIN_STRING = """0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111"""

hex_to_bin = dict([line.split(" = ") for line in HEX_TO_BIN_STRING.strip().split("\n")])


def head_slice(idx=0):
    return slice(idx, idx + 3)


def type_id_slice(idx=0):
    return slice(idx + 3, idx + 6)


def length_type_id_slice(idx=0):
    return slice(idx + 6, idx + 7)


def total_bits_slice(idx=0):
    return slice(idx + 7, idx + 7 + 15)


def num_subpackets_slice(idx=0):
    return slice(idx + 7, idx + 7 + 11)


def stop_after_fail(predicate, iterable):
    while True:
        item = next(iterable)
        if predicate(item):
            yield item
            continue
        else:
            yield item
            break


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return it.zip_longest(*args, fillvalue=fillvalue)


packet_versions = []


@dataclass
class Packet:
    version: int = field(init=False)
    type_id: int = field(init=False)
    value: Optional[int] = None
    subpackets: list["Packet"] = field(default_factory=list)

    def post_init_and_handle_subpackets(self, s):
        self.version = int(s[head_slice()], 2)
        packet_versions.append(self.version)
        self.type_id = int(s[type_id_slice()], 2)
        if self.type_id == 4:  # read literal value
            bit_segments = list(
                stop_after_fail(lambda string: string[0] == "1", grouper(s[6:], 5))
            )
            self.value = int("".join(["".join(seg[1:]) for seg in bit_segments]), 2)
            length = 5 * len(bit_segments)
            return s[6 + length :]

        # not type 4
        self.length_type_id = int(s[length_type_id_slice()], 2)
        if self.length_type_id == 0:
            total_bits = int(s[total_bits_slice()], 2)
            s = s[7 + 15 :]
            length = len(s) - total_bits
            while len(s) > length:
                self.subpackets.append(Packet())
                s = self.subpackets[-1].post_init_and_handle_subpackets(s)
        elif self.length_type_id == 1:
            num_subpackets = int(s[num_subpackets_slice()], 2)
            s = s[7 + 11 :]
            for _ in range(num_subpackets):
                self.subpackets.append(Packet())
                s = self.subpackets[-1].post_init_and_handle_subpackets(s)

        if self.type_id == 0:
            self.value = sum(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 1:
            self.value = prod(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 2:
            self.value = min(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 3:
            self.value = max(subpacket.value for subpacket in self.subpackets)
        elif self.type_id == 5:
            self.value = 1 if self.subpackets[0].value > self.subpackets[1].value else 0
        elif self.type_id == 6:
            self.value = 1 if self.subpackets[0].value < self.subpackets[1].value else 0
        elif self.type_id == 7:
            self.value = (
                1 if self.subpackets[0].value == self.subpackets[1].value else 0
            )

        return s


def part1():
    return sum(packet_versions)


def part2(packet):
    return packet.value


def prepare_input():
    input_ = read_input("16").strip().replace("\n", "")
    return "".join([hex_to_bin[c] for c in input_])


def main():
    raw_packet = prepare_input()
    packet = Packet()
    packet.post_init_and_handle_subpackets(raw_packet)

    print(part1())
    print(part2(packet))


if __name__ == "__main__":
    main()
