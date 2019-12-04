from collections import Counter
from typing import Dict, List, Set, Tuple


def check_meets_criteria(x: int) -> Tuple[bool, bool]:
    passwd = str(x)
    digit_pairs = list(zip(passwd, passwd[1:]))

    same_digits = any(a == b for (a, b) in digit_pairs)
    never_decrease = all(b >= a for (a, b) in digit_pairs)
    no_group = 2 in Counter(passwd).values()

    part1 = same_digits and never_decrease
    part2 = part1 and no_group
    return part1, part2


def main() -> None:
    with open("input.txt") as f:
        inp = tuple(map(int, f.read().strip().split("-")))

    part1, part2 = zip(*[check_meets_criteria(x) for x in range(inp[0], inp[1] + 1)])
    print("Part 1:", sum(part1))
    print("Part 2:", sum(part2))


main()
