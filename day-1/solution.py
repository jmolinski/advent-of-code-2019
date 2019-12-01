def required_fuel(mass):
    return max((mass // 3) - 2, 0)


def part1(inp):
    return sum(required_fuel(module) for module in inp)


def part2(inp):
    def fuel_for_module(m):
        last_added = fuel = required_fuel(m)

        while (to_add := required_fuel(last_added)) > 0:
            fuel += to_add
            last_added = to_add

        return fuel
    
    return sum(fuel_for_module(m) for m in inp)


def main():
    with open("input.txt") as f:
        inp = list(map(int, f.read().split()))

    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))


main()
