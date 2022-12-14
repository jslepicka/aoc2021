from collections import defaultdict

def get_input_pixels(x, y):
    return [(x-1, y - 1), (x, y - 1), (x + 1, y-1), (x - 1, y), (x, y), (x+1, y), (x-1, y+1), (x, y + 1), (x+1, y+1)]

def enhance(algo, input, steps):
    for i in range(steps):
        max_x = max(input, key=lambda p: p[0])[0]
        max_y = max(input, key=lambda p: p[1])[1]
        output = defaultdict(lambda: i & 1)
        for y in range(-1, max_y + 2):
            for x in range(-1, max_x + 2):
                v = 0
                for n in get_input_pixels(x, y):
                    v <<= 1
                    v |= input[n]
                output[(x+1, y+1)] = algo[v]
        input = output
    return(sum(input.values()))

def part1(algo, input):
    return enhance(algo, input, 2)

def part2(algo, input):
    return enhance(algo, input, 50)

def main():
    input = defaultdict(lambda: 0)
    algo = None
    with open("20.txt") as file:
        algo = [int(x) for x in file.readline().strip().replace(".", "0").replace("#", "1")]
        file.readline()
        for y, line in enumerate([x.strip().replace(".", "0").replace("#", "1") for x in file.readlines()]):
            for x, i in enumerate(line):
                input[(x, y)] = int(i)
            
    print("Part 1: " + str(part1(algo, input)))
    print("Part 2: " + str(part2(algo, input)))

if __name__ == "__main__":
    main()
