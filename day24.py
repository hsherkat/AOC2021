# pylint: disable=F0401

from itertools import zip_longest
from typing import NamedTuple, Optional

from utils import read_input


class ALU(dict):
    """Four registers, labeled w, x, y, z.
    Instructions are called on ALUs.
    """

    @classmethod
    def initial(cls) -> "ALU":
        """Initial state is all registers set to 0.
        """
        out = {c: 0 for c in "wxyz"}
        return cls(out)


class Instruction(NamedTuple):
    """Instruction operates on the state of the ALU to produce a new state.
    ALUs will not be mutated.
    """

    args: tuple[str]

    constructors = dict()  # decorator on subcasses will fill this out

    @staticmethod
    def from_str(string: str):
        """Parser.
        """
        name, *args = string.split()
        return Instruction.constructors[name](tuple(args))  # pylint: disable=E1136


def register_instr(cls):
    """Decorator to add constructors to Instruction.
    """
    Instruction.constructors[cls.__name__.lower()] = cls  # pylint: disable=E1137
    return cls


@register_instr
class Inp(Instruction):
    def __call__(self, alu: ALU, val: int):
        var, *_ = self.args
        out = ALU(alu)
        out[var] = val
        return out


@register_instr
class Add(Instruction):
    def __call__(self, alu: ALU):
        var, var_or_val = self.args
        val = alu[var_or_val] if var_or_val.isalpha() else int(var_or_val)
        out = ALU(alu)
        out[var] += val
        return out


@register_instr
class Mul(Instruction):
    def __call__(self, alu: ALU):
        var, var_or_val = self.args
        val = alu[var_or_val] if var_or_val.isalpha() else int(var_or_val)
        out = ALU(alu)
        out[var] *= val
        return out


@register_instr
class Div(Instruction):
    def __call__(self, alu: ALU):
        var, var_or_val = self.args
        val = alu[var_or_val] if var_or_val.isalpha() else int(var_or_val)
        out = ALU(alu)
        out[var] //= val
        return out


@register_instr
class Mod(Instruction):
    def __call__(self, alu: ALU):
        var, var_or_val = self.args
        val = alu[var_or_val] if var_or_val.isalpha() else int(var_or_val)
        out = ALU(alu)
        out[var] = out[var] % val
        return out


@register_instr
class Eql(Instruction):
    def __call__(self, alu: ALU, num: int):
        """The input only calls this for (x w) or (x 0).
        w will be input in execute_block, so just insert it here.
        """
        var, var_or_val = self.args
        val = num if var_or_val.isalpha() else int(var_or_val)
        out = ALU(alu)
        out[var] = int(out[var] == val)
        return out


def execute_block(
    instruction_block: list[Instruction], num: int, initial_alu: Optional[ALU] = None,
) -> ALU:
    output_alu = initial_alu or ALU.initial()
    for instr in instruction_block:
        output_alu = (
            instr(output_alu, num)
            if isinstance(instr, (Inp, Eql))
            else instr(output_alu)
        )
    return output_alu


###########################

"""All that was pointless. Looking at the input, you can do this very simply.
"""


def block_vars(instruction_block: list[Instruction]):
    """Returns z', x', y'.
    """
    vars_ = [int(instruction_block[i].args[-1]) for i in (4, 5, 15)]
    return tuple(vars_)


def fast_execute(
    instruction_block: list[Instruction], w_inp: int, z_initial: int
) -> int:
    zz, xx, yy = block_vars(instruction_block)
    delta = int(z_initial % 26 + xx != w_inp)
    return delta * (w_inp + yy) + (25 * delta + 1) * (z_initial // zz)


##################


def possible_z(zz, xx, yy, z_f, w_inp):
    out = [z_f * zz + r for r in range(zz)]
    if (z_f - w_inp - yy) % 26 == 0:
        out.extend([zz * (z_f - w_inp - yy) // 26 + r for r in range(zz)])
    return out


def backwards(
    block_idx: int,
    instruction_blocks: list[list[Instruction]],
    best_w: dict[int, list[int]],
    max_or_min=max,
):
    new_best = dict()
    zz, xx, yy = block_vars(instruction_blocks[block_idx])
    for z_f, ws in best_w.items():
        for w_inp in range(1, 10):
            for z_i in possible_z(zz, xx, yy, z_f, w_inp):
                if fast_execute(instruction_blocks[block_idx], w_inp, z_i) != z_f:
                    continue
                new_ws = ws[:]
                new_ws[block_idx] = w_inp
                new_best[z_i] = (
                    max_or_min(new_best[z_i], new_ws) if z_i in new_best else new_ws
                )
    return new_best


def part1(instruction_blocks: list[list[Instruction]]):
    cur = {0: [0] * 14}
    for idx in reversed(range(14)):
        cur = backwards(idx, instruction_blocks, cur)
    return "".join(str(n) for n in max(cur.values()))


def part2(instruction_blocks: list[list[Instruction]]):
    cur = {0: [0] * 14}
    for idx in reversed(range(14)):
        cur = backwards(idx, instruction_blocks, cur, min)
    return "".join(str(n) for n in min(cur.values()))


##################


def prepare_input():
    input_ = read_input("24").strip().split("\n")
    inp_idx = [i for i, line in enumerate(input_) if line.startswith("inp")]
    instructions = [Instruction.from_str(line) for line in input_]
    instruction_blocks = [
        instructions[a:b] for a, b in zip_longest(inp_idx, inp_idx[1:])
    ]
    return instruction_blocks


def main():
    instruction_blocks = prepare_input()
    print(part1(instruction_blocks))
    print(part2(instruction_blocks))


##################

if __name__ == "__main__":
    main()


"""
Instructions come in blocks, separated by input. All have the same structure:

w   x   y   z                       inp w
w   0   y   z                       mul x 0
w   z   y   z                       add x z
w   z%26   y   z                    mod x 26
w   z%26   y   z//z'                div z z'
w   z%26+x'   y   z//z'             add x x'
w   0,1   y   z//z'                 eql x w
w   1,0   y   z//z'                 eql x 0
w   1,0   0   z//z'                 mul y 0
w   1,0   25   z//z'                add y 25
w   1,0   25,0   z//z'              mul y x
w   1,0   25,0 + 1  z//z'           add y 1
w   1,0   25,0 + 1  25,0 * z//z'    mul z y
w   1,0   0  25,0 * z//z'           mul y 0
w   1,0   w  25,0 * z//z'           add y w
w   1,0   w+y'  25,0 * z//z'        add y y'
w   1,0   1,0 * w+y'  25,0 * z//z'            mul y x
w   1,0   1,0 * w+y'  d*(w+y') + (25d + 1) * z//z'            add z y


d*(w+y') + (25d + 1) * (z//z')

d = 1   if (z%26) + x' != w
  = 0   if (z%26) + x' == w

the new z value will be:
z//z' if d==0
else
w+y' + 26(z//z')



working backwards from z_final to z_initial:

d==0
z_i//z' = z_f

z_i = z_f*z' + r     r < z'


d==1
w+y' + 26(z_i//z') = z_f
26(z_i//z') = z_f - w - y'
z_f - w - y' must be divisible by 26
z_i//z' = (z_f - w - y')/26

z_i = z' * (z_f - w - y')/26 + r     r < z'
"""
