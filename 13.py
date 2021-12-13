def draw(input):
    width = max(input, key=lambda p: p[0])[0] + 1
    height = max(input, key=lambda p: p[1])[1] + 1

    for y in range(height):
        for x in range(width):
            if (x, y) in input:
                print("#", end="")
            else:
                print(" ", end="")
        print()

def fold(input, instruction):
    axis, loc = instruction.split("=")
    loc = int(loc)
    old_points = []
    new_points = []
    axis = ord(axis) - ord("x")
    for p in input:
        if p[axis] > loc:
            p2 = list(p)
            p2[axis] = p2[axis] - (p2[axis] - loc) * 2
            p2 = tuple(p2)
            old_points.append(p)
            new_points.append(p2)
            
    for p in new_points:
        input[p] = 1
    for p in old_points:
        input.pop(p)  

def part1(input, folds):
    input = input.copy()
    fold(input, folds[0])
    return len(input)

def part2(input, folds):
    input = input.copy()
    for f in folds:
        fold(input, f)         
    draw(input)
    return None

def main():
    input = {}
    folds = []
    with open("13.txt") as file:
        section = 0
        for line in [x.strip() for x in file.readlines()]:
            if line == "":
                section += 1
                continue
            if section == 0:
                x, y = line.split(",")
                input[(int(x),int(y))] = 1
            else:
                folds.append(line.split(" ")[2])

    print("Part 1: " + str(part1(input, folds)))
    print("Part 2: " + str(part2(input, folds)))

if __name__ == "__main__":
    main()
