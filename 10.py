def process_line(line):
    openers = list("([{<")
    closers = list(")]}>")
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    stack = []
    corrupted = False
    corrupted_score = None
    incomplete_score = None
    for c in list(line):
        if c in openers:
            stack.append(c)
        elif c in closers:
            if stack.pop() != openers[closers.index(c)]:
                corrupted = True
                break
        else:
            return None, None
    if corrupted:
        corrupted_score = points[c]
    else:
        incomplete_score = 0
        for i in reversed(stack):
            incomplete_score *= 5
            incomplete_score += openers.index(i) + 1
    return corrupted_score, incomplete_score

def part1(input):
    score = 0
    for line in input:
        s, _ = process_line(line)
        if s:
            score += s
    return score

def part2(input):
    scores = []
    for line in input:
        _, s = process_line(line)
        if s:
            scores.append(s)

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
