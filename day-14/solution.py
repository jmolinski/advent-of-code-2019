from __future__ import annotations
from typing import Callable


def calculate_cost(
    recipes: dict[str, tuple[int, dict[str, int]]], wanted_fuel: int
) -> int:
    ore = 0
    have = {name: 0 for name in recipes}
    have["FUEL"] = -wanted_fuel

    while any(v < 0 for v in have.values()):
        for name in have:
            while have[name] < 0:
                output, ingredients = recipes[name]

                times = (-have[name]) // output
                if times * output < (-have[name]):
                    times += 1

                have[name] += output * times
                for iname, iamount in ingredients.items():
                    if iname == "ORE":
                        ore += iamount * times
                    else:
                        have[iname] -= iamount * times

    return ore


def input_pair(s: str) -> tuple[str, int]:
    num, name = s.strip().split()
    return name.strip(), int(num)


def binsearch(
    value: int, fun: Callable[[int], int], low: int = 0, high: int = 100_000_000
) -> int:
    midpoint = (low + high) // 2
    v_midpoint = fun(midpoint)
    if v_midpoint < value <= fun(midpoint + 1):
        return midpoint

    if v_midpoint > value:
        return binsearch(value, fun, low, midpoint)
    return binsearch(value, fun, midpoint, high)


def main() -> None:
    with open("input.txt") as f:
        inp = [[a.strip() for a in l.split("=>")] for l in f.read().strip().split("\n")]
        recipes = {}
        for inputs, output in inp:
            name, amount = input_pair(output)
            recipes[name] = (amount, dict(input_pair(i) for i in inputs.split(",")))

    print("Part 1:", calculate_cost(recipes, wanted_fuel=1))
    print(
        "Part 2:",
        binsearch(1_000_000_000_000, lambda a: calculate_cost(recipes, wanted_fuel=a)),
    )


main()
