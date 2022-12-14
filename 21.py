import functools

def part1(input):
    p1score = 0
    p2score = 0
    p1pos = input[0]
    p2pos = input[1]
    dieval = 1
    done = 0
    rolls = 0
    while True:
        for _ in range(3):
            rolls += 1
            p1pos = (p1pos + dieval - 1) % 10 + 1
            dieval += 1
            if dieval == 101:
                dieval = 1
        p1score += (p1pos)
        if p1score >= 1000:
            done = 1
            break
        for _ in range(3):
            rolls += 1
            p2pos = (p2pos + dieval - 1) % 10 + 1
            dieval += 1
            if dieval == 101:
                dieval = 1
        p2score += (p2pos)
        if p2score >= 1000:
            done = 1
            break
        if done:
            break
    return min(p1score, p2score) * rolls
        
@functools.lru_cache(maxsize=None)
def roll(p1pos, p1score, p2pos, p2score):
    win1 = 0
    win2 = 0
    if p1score >= 21:
        return (1, 0)
    if p2score >= 21:
        return (0, 1)
    
    for x in range(1, 4):
        for y in range(1, 4):
            for z in range(1, 4):
                newp1pos = (p1pos + x + y + z - 1) % 10 + 1
                newp1score = p1score + newp1pos
                w2, w1 = roll(p2pos, p2score, newp1pos, newp1score)
                win2 += w2
                win1 += w1
    return win1, win2

def part2(input):
    p1start = input[0]
    p2start = input[1]
    wins = roll(p1start, 0, p2start, 0)
    return max(wins)


def main():
    input = []
    with open("21.txt") as file:
        input.append(int(file.readline().strip().split(": ")[1]))
        input.append(int(file.readline().strip().split(": ")[1]))

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()


 
