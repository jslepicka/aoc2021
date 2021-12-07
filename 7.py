def calc_fuel(input, model="linear"):
    min_cost = None
    get_fuel_cost = None

    if model == "linear":
        get_fuel_cost = lambda d: d
    elif model == "quadratic":
        get_fuel_cost = lambda d: .5 * d*d + .5 * d
    else:
        return None
    
    for pos in range(min(input), max(input) + 1):
        cost = 0
        for i in input:
            cost += get_fuel_cost(abs(i - pos))
        if (min_cost is None or cost < min_cost):
            min_cost = cost
        elif cost > min_cost:
            break
    return min_cost

def part1(input):
    return calc_fuel(input)

def part2(input):
    return calc_fuel(input, model="quadratic")

def main():
    input = []
    with open("7.txt") as file:
        for x in file.readlines():
            input = [int(x) for x in x.split(",")]

    print("Part 1: %d" % part1(input))
    print("Part 2: %d" % part2(input))

if __name__ == "__main__":
    main()
