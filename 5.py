from collections import defaultdict

def generate_map(input, include_diagonals=False):
    map = defaultdict(lambda: 0)
    for i in input:
        x1, x2 = i[0][0], i[1][0]
        y1, y2 = i[0][1], i[1][1]
        start = None
        end = None
        if x1 > x2:
            start = i[1]
            end = i[0]
        else:
            start = i[0]
            end = i[1]
        x_delta = end[0] - start[0]
        y_delta = end[1] - start[1]
        x1, x2 = start[0], end[0]
        y1, y2 = start[1], end[1]
        x, y = x1, y1

        d = max(abs(x2-x1), abs(y2-y1))
        if include_diagonals or x1 == x2 or y1 == y2:
            for _ in range(d+1):
                map[(x,y)] += 1
                x += x_delta/d
                y += y_delta/d
    return map

def part1(input):
    map = generate_map(input)
    return sum(value > 1 for value in map.values())

def part2(input):
    map = generate_map(input, include_diagonals=True)
    return sum(value > 1 for value in map.values())

def main():
    input = []
    with open("5.txt") as file:
        for x in [x.strip() for x in file.readlines()]:
            l = x.split()
            x1, y1 = l[0].split(",")
            x2, y2 = l[2].split(",")
            input.append([(int(x1), int(y1)), (int(x2), int(y2))])
    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
