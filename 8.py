def part1(input):
    right_input = []
    for line in input:
        i = line.split("|")
        right_input.append(i[1].split())
    s = 0
    for x in right_input:
        for p in x:
            l = len(p)
            if l <= 4 or l == 7:
                s += 1
    return s

def part2(input):
    # we know which patterns 1, 4, 7, and 8 are
    # for the others, we can see how they differ from the known patterns
    # for example, 9 has 6 segments and shares two segments with 1, 4 segments
    # with 4, and 3 segments with 7.  So we can subtract set(pattern 4) from
    # set(pattern 9) and if the result is 2 remaining, we know that pattern is 9.
    # Repeat with other 6 segment numbers, chosing an appropriate/most specific
    # set to compare to.  Common segments:
    #       1	4	7	8
    #   0	2	3	3	6
    #   2	1	2	2	5
    #   3	2	3	3	5
    #   5	1	3	2	5
    #   6	1	3	2	6
    #   9	2	4	3	6

    s = 0
    for line in input:
        patterns = []
        output = []
        l, r = line.split("|")
        for x in l.split():
            x = [c for c in x]
            x.sort()
            patterns.append("".join(x))
        for x in r.split():
            x = [c for c in x]
            x.sort()
            output.append("".join(x))
        patterns.sort(key=lambda x: len(x))

        sets = [0] * 8
        digits = {}

        for p in patterns:
            if len(p) == 2:
                sets[1] = set([x for x in p])
                digits[p] = 1
            elif len(p) == 3:
                sets[7] = set([x for x in p])
                digits[p] = 7
            elif len(p) == 4:
                sets[4] = set([x for x in p])
                digits[p] = 4
            elif len(p) == 7:
                digits[p] = 8
            else:
                a = set([x for x in p])
                if len(p) == 5:
                    if len(a - sets[7]) == 2:
                        digits[p] = 3
                    elif len(a - sets[4]) == 2:
                        digits[p] = 5
                    else:
                        digits[p] = 2
                elif len(p) == 6:
                    if len(a - sets[4]) == 2:
                        digits[p] = 9
                    elif len(a - sets[7]) == 4:
                        digits[p] = 6
                    else:
                        digits[p] = 0
        out = 0
        for o in output:
            out *= 10
            out += digits[o]
        s += out

    return s

def main():
    input = []
    with open("8.txt") as file:
       input = [x.strip() for x in file.readlines()]

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
