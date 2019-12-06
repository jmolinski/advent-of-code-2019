from typing import List, NoReturn, Tuple, Dict, Tuple
from collections import defaultdict
import itertools


def part1(inp: List[Tuple[str, str]]) -> int:
    all_objects = set(itertools.chain.from_iterable(inp))
    object_being_orbited = {b: a for (a, b) in inp}
    objects_orbits_count = {a: 0 for a in all_objects}

    referenced = set(object_being_orbited.values())
    to_visit = all_objects - referenced
    visited = set()

    while to_visit:
        x = to_visit.pop()
        to_zasil = object_being_orbited[x]

        objects_orbits_count[to_zasil] += objects_orbits_count[x] + 1

        visited.add(x)
        referenced = set(object_being_orbited.values())
        to_visit = all_objects - (visited | referenced | {'COM'})

    return sum(objects_orbits_count.values())


def part2(inp: List[Tuple[str, str]]) -> int:
    object_being_orbited = {b: a for (a, b) in inp}

    def path_to_com(curr: str) -> Dict[str, int]:
        path, i = {}, 1

        while curr != "COM":
            path[curr] = i
            i += 1
            curr = object_being_orbited[curr]

        return path

    you = path_to_com(object_being_orbited["YOU"])
    san = path_to_com(object_being_orbited["SAN"])
    intersect = set(you) & set(san)

    return min(you[i] + san[i] for i in intersect) - 2


def main() -> None:
    with open("input.txt") as f:
        inp = list(
            map(
                lambda l: (l[0], l[1]),
                [x.strip().split(")") for x in f.read().strip().split()],
            )
        )

    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))


main()
