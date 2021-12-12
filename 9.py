from collections import defaultdict

def get_neighbors(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def get_low_points(input):
    low_points = []
    width = max(input, key=lambda p: p[0])[0] + 1
    height = max(input, key=lambda p: p[1])[1] + 1
    for y in range(height):
        for x in range(width):
            p = (x, y)
            v = input[p]
            low = True
            for n in get_neighbors(*p):
                if not v < input[n]:
                    low = False
                    break
            if low:
                low_points.append(p)
    return low_points

def part1(input):
    result = 0
    for p in get_low_points(input):
        result += input[p] + 1
    return result

def get_basin_depth(input, low_point):
    stack = []
    visited = {}
    #DFS
    stack.append(low_point)
    while stack:
        p = stack.pop()
        if p in visited:
            continue
        visited[p] = 1
        for n in get_neighbors(*p):
            if input[n] < 9:
                stack.append(n)
    return len(visited)

def part2(input):
    depths = []
    for p in get_low_points(input):
        depths.append(get_basin_depth(input, p))
    depths.sort(reverse=True)
    result = 1
    for i in range(3):
        result *= depths[i]
    return result

def main():
    input = defaultdict(lambda: 10)
    with open("9.txt") as file:
        y = 0
        for line in [x.strip() for x in file.readlines()]:
            x = 0
            for i in list(line):
                input[(x, y)] = int(i)
                x += 1
            y += 1

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
