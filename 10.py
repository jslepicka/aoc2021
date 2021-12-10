def part1(input):
    openers = list("([{<")
    closers = list(")]}>")
    illegal_chars = []
    for line in input:
        stack = []
        for c in list(line):
            if c in openers:
                stack.insert(0, c)
            elif c in closers:
                d = stack.pop(0)
                closer_index = closers.index(c)
                if d != openers[closer_index]:
                    illegal_chars.append(c)
            else:
                return None
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    score = sum([points[x] for x in illegal_chars])
    return score

def part2(input):
    incomplete = []
    openers = list("([{<")
    closers = list(")]}>")

    scores = []
    for line in input:
        stack = []
        corrupted = False
        for c in list(line):
            if c in openers:
                stack.insert(0, c)
            elif c in closers:
                if stack.pop(0) != openers[closers.index(c)]:
                    corrupted = True
                    break
            else:
                return None
        if corrupted:
            continue
        score = 0
        for i in stack:
            score *= 5
            score += openers.index(i) + 1
        scores.append(score)
    scores.sort()
    median_score = scores[len(scores)//2]
    return median_score

def main():
    input = []
    with open("10.txt") as file:
        input = [x.strip() for x in file.readlines()]

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
