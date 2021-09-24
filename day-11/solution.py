from __future__ import annotations

from typing import Any, Callable, List, NoReturn, Optional, Tuple


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
            9: (self.op_9, 2),
        }

        self.relative_base = 0

    def run(self, op: int) -> Callable[[int, List[int]], int]:
        def wrapper(pos: int, modes: List[int]) -> int:
            fn, length = self.operations[op]
            ret = fn(pos, modes)
            return pos + length if ret is None else ret

        return wrapper

    def mode_aware_get(self, mode: int, pos: int) -> int:
        if mode == 0:
            return self.mem[self.mem[pos]]
        elif mode == 1:
            return self.mem[pos]
        else:  # mode 2
            return self.mem[self.relative_base + self.mem[pos]]

    def mode_aware_set(self, mode: int, pos: int, val: int) -> None:
        if mode == 0:
            self.mem[self.mem[pos]] = val
        elif mode == 1:
            raise ValueError
        else:  # mode 2
            self.mem[self.relative_base + self.mem[pos]] = val

    def op_1(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mode_aware_set(modes[2], pos + 3, a + b)

    def op_2(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mode_aware_set(modes[2], pos + 3, a * b)

    def op_3(self, pos: int, modes: List[int]) -> Optional[int]:
        if not self.vm.inputs:
            if self.vm.halt_on_empty_input:
                self.vm.halt = True
                return pos

        self.mode_aware_set(modes[0], pos + 1, self.vm.inputs.pop(0))
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
        self.mode_aware_set(modes[2], pos + 3, 1 if a < b else 0)

    def op_8(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        b = self.mode_aware_get(modes[1], pos + 2)
        self.mode_aware_set(modes[2], pos + 3, 1 if a == b else 0)

    def op_9(self, pos: int, modes: List[int]) -> None:
        a = self.mode_aware_get(modes[0], pos + 1)
        self.relative_base += a

    def op_99(self, pos: int, modes: List[int]) -> NoReturn:
        raise StopIteration


class VM:
    def __init__(self, mem: List[int], *, halt_on_empty_input=False) -> None:
        self.mem = mem[:]
        self.mem = self.mem + [0 for _ in range(20000)]
        self.inputs: List[int] = []
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

    def clear_output(self) -> None:
        self.outputs = []


BLACK, WHITE = 0, 1


def run_robot(inp: List[int], starting_color: int) -> dict:
    # Board indexing:
    # (1, 0) (1, 1)
    # (0, 0) (0, 1)
    up, down, left, right = (1, 0), (-1, 0), (0, -1), (0, 1)
    right_turn = {up: right, right: down, down: left, left: up}
    left_turn = {up: left, left: down, down: right, right: up}

    position = (0, 0)
    move_vector = up
    tile_colors = {position: starting_color}

    vm = VM(inp, halt_on_empty_input=True)

    vm.exec(inputs=[])
    while not vm.is_finished:
        vm.clear_output()
        _, [color_to_paint, turn_direction] = vm.resume(
            inputs=[tile_colors.get(position, BLACK)]
        )

        tile_colors[position] = color_to_paint
        move_vector = (left_turn if turn_direction == 0 else right_turn)[move_vector]

        position = (position[0] + move_vector[0], position[1] + move_vector[1])

    return tile_colors


def part1(inp: List[int]) -> int:
    return len(run_robot(inp, BLACK))


def part2(inp: List[int]) -> None:
    tiles = run_robot(inp, WHITE)

    min_x, max_x = min(x for (y, x) in tiles), max(x for (y, x) in tiles)
    min_y, max_y = min(y for (y, x) in tiles), max(y for (y, x) in tiles)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            color = "   "
            if tiles.get((y, x)) == WHITE:
                color = "[X]"
            print(color, end="")
        print()


def main() -> None:
    with open("input.txt") as f:
        inp = list(map(int, f.read().strip().split(",")))

    print("Part 1:", part1(inp))
    print("Part 2:")
    part2(inp)


main()
