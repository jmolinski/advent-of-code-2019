import cmath
import itertools
from typing import List, Set, Tuple

Point = Tuple[int, int]


def dst(a: Point, b: Point) -> float:
    (x1, y1), (x2, y2) = (a, b)
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def group_asteroids(a: Point, asteroids: Set[Point]) -> List[List[Tuple[float, Point]]]:
    x, y = a

    def slope(p: Point) -> float:
        x1, y1 = p
        xp, yp = x1 - x, y1 - y  # change (0, 0) -> (x, y)
        r, phi = cmath.polar(complex(xp, yp) / complex(0, 1))  # rotate -pi/2
        return phi

    slope_dst_point = [(slope(p), dst((x, y), p), p) for p in asteroids - {(x, y)}]
    slope_dst_point.sort(key=lambda x: x[1])  # timsort is stable: sort by (x[0], x[1])
    slope_dst_point.sort(key=lambda x: x[0])

    return [
        [(a[1], a[2]) for a in x]
        for (_, x) in itertools.groupby(slope_dst_point, key=lambda x: x[0])
    ]


def solution(inp: List[str]) -> Tuple[int, int]:
    rows, cols = len(inp), len(inp[0])
    asteroids = set(
        itertools.chain.from_iterable(
            [[(x, y) for x in range(rows) if inp[y][x] == "#"] for y in range(cols)]
        )
    )

    max_visible = max([group_asteroids(a, asteroids) for a in asteroids], key=len)

    _, (x, y) = max_visible[199 % len(max_visible)][199 // len(max_visible)]

    return len(max_visible), 100 * x + y


def main() -> None:
    with open("input.txt") as f:
        inp = f.read().strip().split()

    part1, part2 = solution(inp)
    print("Part 1:", part1)
    print("Part 2:", part2)


main()
