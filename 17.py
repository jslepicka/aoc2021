from math import sqrt, floor, ceil

def part1(input):
    answer = 0
    for yv in range(200):
        yv2 = yv
        y = 0
        last_y = 0
        max_y = 0
        hit = False
        for _ in range(500):
            y += yv2
            if y < input[2]:
                break
            if y >= input[2] and y <= input[3]:
                hit = True
            yv2 -= 1
            if y == last_y:
                max_y = y
            last_y = y
        if hit:
            if max_y > answer:
                answer = max_y
    return answer

def part2(input):
    hits = set()
    min_x = 0
    max_x = input[1]
    for xv in range(min_x, max_x + 1):
        for yv in range(input[2], 200):
            start_x = xv
            start_y = yv
            xv2 = xv
            yv2 = yv
            x = 0
            y = 0
            hit = False
            for _ in range(500):
                x += xv2
                y += yv2
                if y < input[2]:
                    break
                if x >= input[0] and x <= input[1] and y >= input[2] and y <= input[3]:
                    hit = True
                if xv2 > 0:
                    xv2 -= 1
                yv2 -= 1
            if hit:
                hits.add((start_x, start_y))
    return len(hits)

def main():
    input = []
    with open("17.txt") as file:
        l = file.readline().strip()
        l = l.split("=")
        x = [int(a) for a in l[1].split(",")[0].split("..")]
        y = [int(a) for a in l[2].split("..")]
        input = list((*x, *y))

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
