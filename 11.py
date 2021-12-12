from collections import defaultdict

neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def draw(input):
    width = max(input, key=lambda p: p[0])[0] + 1
    height = max(input, key=lambda p: p[1])[1] + 1
    for y in range(height):
        for x in range(width):
            e = input[(x, y)]
            if e != -1:
                print(e, end="")
        print()

def inc_energy(input):
    flash_count = 0
    flashes = []
    for i in input:
        e = input[i]
        if input[i] != -1:
            e += 1
            input[i] = e
            if e == 10:
                flashes.append(i)
    while flashes:
        new_flashes = []
        for f in flashes:
            flash_count += 1
            input[f] = 99
            for n in neighbors:
                x = f[0] + n[0]
                y = f[1] + n[1]
                e = input[(x, y)]
                if e != -1:
                    e += 1
                    input[(x, y)] = e
                    if e == 10:
                        new_flashes.append((x, y))
        flashes = new_flashes
    for i in input:
        if input[i] > 9:
            input[i] = 0
    return flash_count

def part1(input):
    input = input.copy()
    total_flashes = 0
    for _ in range(100):
        total_flashes += inc_energy(input)
    return total_flashes

def part2(input):
    input = input.copy()
    step = 0
    while True:
        step += 1
        flash_count = inc_energy(input)
        if flash_count == 100:
            return step

def main():
    input = defaultdict(lambda: -1)
    with open("11.txt") as file:
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
