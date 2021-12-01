def part1(input):
    prev = None
    depth = 0
    for m in input:
        if prev is not None and m > prev:
            depth += 1
        prev = m
    return depth

def part2(input):
    sums = [sum(input[i:i+3]) for i in range(0, len(input)-2)]
    return part1(sums)

def main():
    input = []
    with open("1.txt") as file:
        input = [int(x.strip()) for x in file.readlines()]

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
