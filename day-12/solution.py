import itertools
import math
from typing import Dict, Iterable, List, Set, Tuple, cast


def vec_sum(a: Iterable[int], b: Iterable[int]) -> Tuple[int, int, int]:
    return cast(Tuple[int, int, int], tuple([x + y for (x, y) in zip(a, b)]))


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def mkchange(a: int, b: int) -> int:
    if a > b:
        return -1
    if a == b:
        return 0
    return 1


def umoon(
    moon: Tuple[int, int, int],
    moon_vel: Tuple[int, int, int],
    moons: Set[Tuple[int, int, int]],
) -> Tuple[int, int, int]:
    x, y, z = moon
    xc, yc, zc = moon_vel
    for m in moons:
        dx, dy, dz = m
        xc, yc, zc = xc + mkchange(x, dx), yc + mkchange(y, dy), zc + mkchange(z, dz)

    return (xc, yc, zc)


def update_velocities(
    v_m: Dict[Tuple[int, int, int], Tuple[int, int, int]]
) -> Dict[Tuple[int, int, int], Tuple[int, int, int]]:
    ks = set(v_m.keys())
    mp = {m: ks - {m} for m in ks}
    return {m: umoon(m, v_m[m], mp[m]) for m in mp}


def energy(m: Tuple[int, int, int], v: Tuple[int, int, int]) -> int:
    (x, y, z), (a, b, c) = m, v
    pot = abs(x) + abs(y) + abs(z)
    kin = abs(a) + abs(b) + abs(c)
    return pot * kin


def part1(inp: List[Tuple[int, int, int]]) -> int:
    v_m = {m: (0, 0, 0) for m in inp}

    for step in range(1000):
        v_m = update_velocities(v_m)
        v_m = {vec_sum(m, v): v for (m, v) in v_m.items()}  # apply velocity

    return sum(energy(m, k) for m, k in v_m.items())


def coordinate_repeats_after(inp: Iterable[int]) -> int:
    v_m = [(m, 0) for m in inp]

    first = tuple(v_m)
    for step in itertools.count(1):
        v_m = [
            (m, v + sum(mkchange(m, dx) for dx in moons))
            for ((m, v), moons) in [(m, [x[0] for x in v_m if x != m]) for m in v_m]
        ]
        v_m = [(m + v, v) for (m, v) in v_m]  # apply velocity
        if first == tuple(v_m) and step > 1:
            return step
    return -1


def part2(inp: List[Tuple[int, int, int]]) -> int:
    coords = list(itertools.chain.from_iterable(inp))
    x, y, z = coords[::3], coords[1::3], coords[2::3]

    return lcm(
        coordinate_repeats_after(x),
        lcm(coordinate_repeats_after(y), coordinate_repeats_after(z)),
    )


def main() -> None:
    inp = [(16, -11, 2), (0, -4, 7), (6, 4, -10), (-3, -2, -4)]

    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))


main()
