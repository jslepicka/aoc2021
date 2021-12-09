from collections import defaultdict
neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def add_points(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def get_low_points(input):
    low_points = []
    width = max(input, key=lambda p: p[0])[0] + 1
    height = max(input, key=lambda p: p[1])[1] + 1
    for y in range(height):
        for x in range(width):
            p = (x, y)
            v = input[p]
            low = True
            for n in range(4):
                if not v < input[add_points(p, neighbors[n])]:
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
    queue = []
    visited = {}
    #DFS
    queue.append(low_point)
    while queue:
        p = queue.pop(0)
        visited[p] = 1
        for n in range(4):
            p2 = (add_points(p, neighbors[n]))
            if input[p2] < 9 and p2 not in visited:
                queue.insert(0, p2)
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
