def part1(input):
    h = 0
    d = 0
    for i in input:
        if (i[0] == "forward"):
            h += int(i[1])
        elif (i[0] == "down"):
            d += int(i[1])
        elif (i[0] == "up"):
            d -= int(i[1])

    return h * d

def part2(input):
    h = 0
    d = 0
    aim = 0
    for i in input:
        if (i[0] == "forward"):
            x = int(i[1])
            h += x
            d += aim * x
        elif (i[0] == "down"):
            aim += int(i[1])
        elif (i[0] == "up"):
            aim -= int(i[1])
    return h*d

def main():
    input = []
    with open("2.txt") as file:
        input = [x.strip().split(" ") for x in file.readlines()]

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
