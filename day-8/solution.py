from itertools import zip_longest
from typing import Any, Iterable, List


def grouper(iterable: Iterable[Any], n: int):
    args = [iter(iterable)] * n
    return zip_longest(*args)


def part1(inp: List[int]) -> int:
    layers = grouper(inp, 25 * 6)
    minimum_zeroes_layer = min(layers, key=lambda x: x.count(0))
    return minimum_zeroes_layer.count(1) * minimum_zeroes_layer.count(2)


def part2(inp: List[int]) -> None:
    layers = grouper(inp, 25 * 6)
    layer_size = 25 * 6

    image = [2 for _ in range(25 * 6)]

    # (1st layers is on top, the highest placed non-transparent (2) pixel is visible)
    for layer in layers:
        for pos, px in enumerate(layer):
            if image[pos] == 2:
                image[pos] = px

    for row in grouper(image, 25):
        print("".join(map(str, row)).replace("1", "1").replace("0", " "))


def main() -> None:
    with open("input.txt") as f:
        inp = list(map(int, f.read().strip()))

    print("Part 1:", part1(inp))
    print("Part 2:")
    part2(inp)


main()
