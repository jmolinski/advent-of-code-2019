from typing import List, Tuple, Set, Dict


def add_vec(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] + v2[0], v1[1] + v2[1]


def map_moves(steps: List[Tuple[str, int]]) -> Dict[Tuple[int, int], int]:
    movement_vec = {
        "U": (1, 0),
        "D": (-1, 0),
        "R": (0, 1),
        "L": (0, -1),
    }

    pos, step = (0, 0), 1

    visited: Dict[Tuple[int, int], int] = {}
    for direction, length in steps:
        for i in range(1, length + 1):
            pos = add_vec(pos, movement_vec[direction])
            visited[pos] = visited.get(pos, step)
            step += 1

    return visited


def part1(inp: List[List[Tuple[str, int]]]) -> int:
    cable1, cable2, *a = inp
    path1, path2 = map_moves(cable1), map_moves(cable2)

    intersections = set(path1.keys()) & set(path2.keys())
    distances = [abs(a) + abs(b) for (a, b) in intersections]

    return min(distances)


def part2(inp: List[List[Tuple[str, int]]]) -> int:
    cable1, cable2, *a = inp
    path1, path2 = map_moves(cable1), map_moves(cable2)

    combined_steps = {
        length + path2[position]
        for position, length in path1.items()
        if position in path2
    }

    return min(combined_steps)


def main() -> None:
    with open("input.txt") as f:
        inp = [
            list(map(lambda o: (o[0], int(o[1:])), x.strip().split(",")))
            for x in f.readlines()
        ]

    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))


main()
