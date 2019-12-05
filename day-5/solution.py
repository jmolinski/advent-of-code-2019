from typing import List, NoReturn


def mode_aware_get(mode, pos, l):
    if mode == 0:
        return l[l[pos]]
    else:
        return l[pos]


def op_1(l: List[int], pos: int, mode_f, mode_s, *args, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)
    b = mode_aware_get(mode_s, pos + 2, l)

    l[l[pos + 3]] = a + b

    return 4 + pos


def op_2(l: List[int], pos: int, mode_f, mode_s, *args, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)
    b = mode_aware_get(mode_s, pos + 2, l)

    l[l[pos + 3]] = a * b

    return 4 + pos


def op_3(
    l: List[int], pos: int, mode_f, mode_s, mode_l, *a, inputs=None, **kwargs
) -> int:
    assert type(inputs) == list
    i = inputs.pop(0)

    l[l[pos + 1]] = i

    return 2 + pos


def op_4(l: List[int], pos: int, mode_f, *a, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)

    print(a)

    return 2 + pos


def op_5(l: List[int], pos: int, mode_f, mode_s, *a, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)
    b = mode_aware_get(mode_s, pos + 2, l)

    if a != 0:
        return b
    else:
        return pos + 3


def op_6(l: List[int], pos: int, mode_f, mode_s, *a, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)
    b = mode_aware_get(mode_s, pos + 2, l)

    if a == 0:
        return b
    else:
        return pos + 3


def op_7(l: List[int], pos: int, mode_f, mode_s, *a, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)
    b = mode_aware_get(mode_s, pos + 2, l)

    l[l[pos + 3]] = 1 if a < b else 0

    return pos + 4


def op_8(l: List[int], pos: int, mode_f, mode_s, *a, **kwargs) -> int:
    a = mode_aware_get(mode_f, pos + 1, l)
    b = mode_aware_get(mode_s, pos + 2, l)

    l[l[pos + 3]] = 1 if a == b else 0

    return pos + 4


def op_99(l: List[int], pos: int, *a, **kwargs) -> NoReturn:
    raise StopIteration


class VM:
    operations = {
        1: op_1,
        2: op_2,
        3: op_3,
        4: op_4,
        5: op_5,
        6: op_6,
        7: op_7,
        8: op_8,
        99: op_99,
    }

    def __init__(self, l: List[int]) -> None:
        self.l = l[:]

    def exec(self, inputs: List[int]) -> List[int]:
        self.inputs = inputs

        p = 0

        try:
            while True:
                p = self.run_op(p)
        except StopIteration:
            return self.l

    def run_op(self, p: int) -> int:
        opcode = "000000" + str(self.l[p])
        
        op = int(opcode[-2:])
        mode_ff = int(opcode[-3])
        mode_f = int(opcode[-4])
        mode_s = int(opcode[-5])

        return self.operations[op](
            self.l, p, mode_ff, mode_f, mode_s, inputs=self.inputs
        )


def main() -> None:
    with open("input.txt") as f:
        inp = list(map(int, f.read().strip().split(",")))

    print("Part 1:", end=" ")
    VM(inp).exec(inputs=[1])
    print("Part 2:", end=" ")
    VM(inp).exec(inputs=[5])


main()
