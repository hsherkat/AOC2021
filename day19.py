# pylint: disable=F0401

from dataclasses import dataclass
from itertools import combinations, product

from utils import read_input

Vector = tuple[int, int, int]


def minus(u: Vector, v: Vector):
    return tuple([ui - vi for ui, vi in zip(u, v)])


def X(v: Vector):
    return (v[0], -v[2], v[1])


def Y(v: Vector):
    return (-v[2], v[1], v[0])


def Z(v: Vector):
    return (-v[1], v[0], v[2])


def compose(fn_seq: list, arg):
    """
    [f,g,h] will do h, then g, then f.
    """
    if not fn_seq:
        return arg
    out = arg
    for f in reversed(fn_seq):
        out = f(out)
    return out


def rotate(rotation_seq: list, v: Vector):
    return compose(rotation_seq, v)


"""
Pick a direction to face and which way is up.

x-axis rotation (any of the 4)
y-axis rotation (any of the 4)
 or
x-axis rotation (any of the 4)
z-axis rotation (+90 or - 90)
"""

reorientations_fns = [[Y] * ky + [X] * kx for kx in range(4) for ky in range(4)]

reorientations_fns.extend([[Z] * kz + [X] * kx for kx in range(4) for kz in (1, 3)])


@dataclass
class Scanner:
    beacons: list[Vector]

    def translate(self, v: Vector):
        """If you move this scanner by v, beacons shift by -v.
        """
        return Scanner([minus(beacon, v) for beacon in self.beacons])

    def rotate(self, rotation_seq: list):
        """If you rotate this scanner by R^-1, beacons rotate by R.
        """
        return Scanner([rotate(rotation_seq, beacon) for beacon in self.beacons])

    def reorientations(self):
        return [self.rotate(rotation_seq) for rotation_seq in reorientations_fns]

    def remap_other(self, other: "Scanner"):
        """If other scanner can be remapped to share 12+ beacons with self,
        return the remapped scanner.
        """
        for base_pt in self.beacons:
            for other_rotated in other.reorientations():
                for overlap_pt in other_rotated.beacons:
                    v_translate = minus(overlap_pt, base_pt)
                    translated = other_rotated.translate(v_translate)
                    overlap = set(self.beacons) & set(translated.beacons)
                    if len(overlap) >= 12:
                        translations.append(v_translate)
                        return translated


def part1(scanners: list[Scanner]):
    known_beacons = set(scanners[0].beacons)
    matches = {0}
    for _ in range(50):
        for (idx1, scanner1), (idx2, scanner2) in product(
            enumerate(scanners), repeat=2
        ):  # scanner1 is known and remapped to scanner[0]; try to match scanner2
            if (idx1 not in matches) or (idx2 in matches):
                continue
            if (remapped := scanner1.remap_other(scanner2)) is not None:
                known_beacons.update(remapped.beacons)
                matches.add(idx2)
                scanners[idx2] = remapped
                break
    return known_beacons


def mhtn_norm(u: Vector, v: Vector):
    return sum(abs(ui - vi) for ui, vi in zip(u, v))


translations = []


def part2(scanners):
    beacons = part1(scanners)
    print(len(beacons))
    return max(mhtn_norm(b1, b2) for b1, b2 in combinations(translations, r=2))


def prepare_input():
    input_ = read_input("19").strip().split("\n\n")
    raw_scanners = [block.strip().split("\n")[1:] for block in input_]
    scanners = [
        [tuple(map(int, line.split(","))) for line in scanner]
        for scanner in raw_scanners
    ]
    return [Scanner(scanner) for scanner in scanners]


def main():
    scanners = prepare_input()
    print(part2(scanners))


test_input = """-- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


if __name__ == "__main__":
    main()
