from collections import Counter
from collections import defaultdict

rules = {}
cache = {}

def count(polymer, depth):
    global cache
    if depth == 0:
        return Counter(polymer)
    key = (polymer, depth)
    if key in cache:
        return cache[key]
    poly_len = len(polymer)
    if poly_len > 2:
        s = Counter()
        for i in range(1, poly_len):
            pair = polymer[i-1] + polymer[i]
            s += count(pair, depth)
        r = s - Counter(polymer[1:-1])
        cache[key] = r
        return r

    new_char = rules[polymer]
    new_polymer = polymer[0] + new_char + polymer[1]
    r = count(new_polymer, depth - 1)
    cache[key] = r
    return r

def part1old(template, rules):
    polymer = template
    for i in range(20):
        new_polymer = ""
        prev = None
        for e in polymer:
            if prev is None:
                new_polymer += e
            else:
                new_polymer += rules[prev+e] + e
            prev = e
        polymer = new_polymer
        counts = Counter(polymer)
    counts = Counter(polymer)
    print(len(polymer))
    return counts.most_common()[0][1] - counts.most_common()[-1][1]

def part1(template):
    c = count(template, 1)
    print(c)
    return c.most_common()[0][1] - c.most_common()[-1][1]

def part2(template):
    c = count(template, 40)
    print(c)
    return c.most_common()[0][1] - c.most_common()[-1][1]

def main():
    template = ""
    global rules
    #rules = {}
    with open("14.txt") as file:
        template = file.readline().strip()
        file.readline()
        for line in file.readlines():
            adj, elem = line.strip().split(" -> ")
            rules[adj] = elem
    
    print("Part 1: " + str(part1(template)))
    print("Part 2: " + str(part2(template)))

if __name__ == "__main__":
    main()
