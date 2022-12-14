from collections import defaultdict

def get_overlap_region(cube1, cube2):
    x1, x2, y1, y2, z1, z2 = cube1
    X1, X2, Y1, Y2, Z1, Z2 = cube2
    if x2 >= X1 and x1 <= X2 and y2 >= Y1 and y1 <= Y2 and z2 >= Z1 and z1 <= Z2:
        xmin = max(x1, X1)
        xmax = min(x2, X2)
        ymin = max(y1, Y1)
        ymax = min(y2, Y2)
        zmin = max(z1, Z1)
        zmax = min(z2, Z2)
        return (xmin, xmax, ymin, ymax, zmin, zmax)
        
    return None

def reboot(input, initialize_only = False):
    regions = defaultdict(lambda: 0)

    for step in input:
        ins, cube = step
        if initialize_only:
            if any([abs(x) > 50 for x in cube]):
                continue

        for prev_cube, val in regions.
        copy().items():
            overlap = get_overlap_region(cube, prev_cube)
            if overlap:
                regions[overlap] -= val

        if ins:
            regions[cube] += 1
        
    s = 0
    for (x1, x2, y1, y2, z1, z2), v in regions.items():
        s += (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1) * v
    return s


def part1(input):
    return reboot(input, initialize_only=True)

def part2(input):
    return reboot(input)

def main():
    input = []
    with open("22.txt") as file:
        for x in [x.strip() for x in file.readlines()]:
            step = []
            ins, coords = x.split(" ")
            ins = 1 if ins == "on" else 0
            for c in coords.split(","):
                c = c.split("=")[1]

                x1, x2 = [int(x) for x in c.split("..")]
                xmin = min(x1, x2)
                xmax = max(x1, x2)
                step.extend([xmin, xmax])

            input.append([ins, tuple(step)])

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
