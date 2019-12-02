from typing import List, NoReturn


def op_1(l: List[int], pos: int) -> int:
    a = l[l[pos + 1]]
    b = l[l[pos + 2]]

    l[l[pos + 3]] = a + b

    return 4


def op_2(l: List[int], pos: int) -> int:
    a = l[l[pos + 1]]
    b = l[l[pos + 2]]

    l[l[pos + 3]] = a * b

    return 4


def op_99(l: List[int], pos: int) -> NoReturn:
    raise StopIteration


class VM:
    operations = {
        1: op_1,
        2: op_2,
        99: op_99,
    }

    def __init__(self, l: List[int]) -> None:
        self.l = l[:]

    def exec(self, noun: int, verb: int) -> List[int]:

        self.l[1] = noun
        self.l[2] = verb

        p = 0

        try:
            while True:
                p = self.run_op(p)
        except StopIteration:
            return self.l

    def run_op(self, p: int) -> int:
        return p + self.operations[self.l[p]](self.l, p)


def part1(inp: List[int]) -> int:
    return VM(inp).exec(12, 2)[0]


def part2(inp: List[int]) -> int:
    for noun in range(100):
        for verb in range(100):
            if VM(inp).exec(noun, verb)[0] == 19690720:
                return 100 * noun + verb
    raise ValueError


def main() -> None:
    with open("input.txt") as f:
        inp = list(map(int, f.read().strip().split(",")))

    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))


main()
