from __future__ import annotations

import itertools
from copy import deepcopy
from typing import Any, Callable, Dict, List, NoReturn, Optional, Tuple


class CPU:
    def __init__(self, vm: VM) -> None:
        self.vm = vm
        self.mem = vm.mem
        self.operations = {
            1: (self.op_1, 4),
            2: (self.op_2, 4),
            3: (self.op_3, 2),
            4: (self.op_4, 2),
            5: (self.op_5, 2),
            6: (self.op_6, 3),
            7: (self.op_7, 4),
            8: (self.op_8, 4),
            99: (self.op_99, 0),
        }

    def run(self, op: int) -> Callable[[int, List[int]], int]:
        def wrapper(pos: int, modes: List[int]) -> int:
            fn, length = self.operations[op]
            ret = fn(pos, modes)
            return pos + length if ret is None else ret

        return wrapper

    def mode_aware_get(self, mode: int, pos: int) -> int:
        return self.mem[self.mem[pos]] if mode == 0 else self.mem[pos]

    def op_1(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mem[self.mem[pos + 3]] = a + b

    def op_2(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mem[self.mem[pos + 3]] = a * b

    def op_3(self, pos: int, modes: List[int]) -> Optional[int]:
        if not self.vm.inputs:
            if self.vm.halt_on_empty_input:
                self.vm.halt = True
                return pos

        self.mem[self.mem[pos + 1]] = self.vm.inputs.pop(0)
        return None

    def op_4(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        self.vm.outputs.append(a)

    def op_5(self, pos: int, modes: List[int]) -> int:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        return b if a != 0 else pos + 3

    def op_6(self, pos: int, modes: List[int]) -> int:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        return b if a == 0 else pos + 3

    def op_7(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mem[self.mem[pos + 3]] = 1 if a < b else 0

    def op_8(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mem[self.mem[pos + 3]] = 1 if a == b else 0

    def op_99(self, pos: int, modes: List[int]) -> NoReturn:
        raise StopIteration


class VM:
    def __init__(
        self, l: List[int], phase: Optional[int] = 0, *, halt_on_empty_input=False
    ) -> None:
        self.mem = l[:]
        self.inputs: List[int] = []
        if phase is not None:
            self.inputs.append(phase)
        self.halt_on_empty_input = halt_on_empty_input
        self.halt = False
        self.outputs: List[int] = []
        self.p = 0
        self.is_finished = False

        self.cpu = CPU(self)

    def exec(
        self, inputs: List[int], *, init_p: int = 0
    ) -> Tuple[List[int], List[int]]:
        self.inputs += inputs
        self.p = init_p

        try:
            while True:
                self.p = self.run_op(self.p)
                if self.halt:
                    return self.mem, self.outputs
        except StopIteration:
            self.is_finished = True
            return self.mem, self.outputs

    def resume(self, inputs: List[int]) -> Tuple[List[int], List[int]]:
        self.halt = False
        return self.exec(inputs, init_p=self.p)

    def run_op(self, p: int) -> int:
        opcode = "0000" + str(self.mem[p])

        op = int(opcode[-2:])
        modes = [int(opcode[-3]), int(opcode[-4]), int(opcode[-5])]

        return self.cpu.run(op)(p, modes)


def part1(inp: List[int]) -> int:
    outputs = []
    for (a, b, c, d, e) in itertools.permutations([0, 1, 2, 3, 4]):
        _, out = VM(inp, a).exec(inputs=[0])
        _, out = VM(inp, b).exec(inputs=[out[0]])
        _, out = VM(inp, c).exec(inputs=[out[0]])
        _, out = VM(inp, d).exec(inputs=[out[0]])
        _, out = VM(inp, e).exec(inputs=[out[0]])
        outputs.append(out[0])

    return max(outputs)


def part2(inp: List[int]) -> int:
    outputs = []
    for (a, b, c, d, e) in itertools.permutations([5, 6, 7, 8, 9]):
        vms = [vm0, vm1, vm2, vm3, vm4] = [
            VM(inp, phase=x, halt_on_empty_input=True) for x in [a, b, c, d, e]
        ]

        out = [0]
        while not vm4.is_finished:
            for i, vm in enumerate(vms):
                _, out = vm.resume(inputs=out)
                vm.outputs = []

        outputs.append(out[-1])

    return max(outputs)


def main() -> None:
    with open("input.txt") as f:
        inp = list(map(int, f.read().strip().split(",")))

    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))


main()
