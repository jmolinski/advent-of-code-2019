import math
from typing import Dict, List, Tuple


def required_ore(
    ingredients: Dict[str, Tuple[int, List[Tuple[int, str]]]], fuel: int
) -> int:
    required = {"FUEL": fuel}
    stock: Dict[str, int] = {}
    while {k for k, v in required.items() if v > 0} != {"ORE"}:
        next_required = next(k for k in required if k != "ORE")
        required_amount = required.pop(next_required)

        amount, required_ingredients = ingredients[next_required]
        multiplier = math.ceil(required_amount / amount)

        for ing_amount, ingredient in required_ingredients:
            amnt = ing_amount * multiplier
            if ingredient in stock:
                to_rm = min(stock[ingredient], amnt)
                stock[ingredient] -= to_rm
                amnt -= to_rm
                if stock[ingredient] == 0:
                    stock.pop(ingredient)

            if amnt:
                required[ingredient] = amnt + required.get(ingredient, 0)

        if (left_over := amount * multiplier - required_amount) :
            stock[next_required] = left_over + stock.get(next_required, 0)

    return required["ORE"]


def part2(ingredients: Dict[str, Tuple[int, List[Tuple[int, str]]]]) -> int:
    ore = 1000000000000
    lo, hi = 2, ore

    while lo < hi:
        mid = (lo + hi) // 2
        if ore < required_ore(ingredients, mid):
            hi = mid
        else:
            lo = mid + 1

    return lo - 1


def main() -> None:
    with open("input.txt") as f:
        inp = [
            x.split()
            for x in f.read().strip().replace(",", "").replace("=>", "").split("\n")
        ]
        ingredients: Dict[
            str, Tuple[int, List[Tuple[int, str]]]
        ] = {  # product -> (amount, lst of (amount, ingredient) )
            r[-1][1]: (r[-1][0], r[:-1])
            for r in [list(zip(map(int, r[::2]), r[1::2])) for r in inp]
        }

    print("Part 1:", required_ore(ingredients, 1))
    print("Part 2:", part2(ingredients))


main()
