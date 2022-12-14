import re
from math import ceil, floor
        
def bisect(string, start, end):
    return string[:start], string[end:]

def explode2(number):
    for m in re.finditer(r'\[(\d+),(\d+)\]', number):
        left_count = number[m.start()+1:].count('[')
        right_count = number[m.start()+1:].count(']')
        depth = right_count - left_count
        if depth > 4:
            left_half, right_half = bisect(number, m.start(), m.end())
            m2 = re.search(r'(\d+)[^\d]*$', left_half)
            if m2:
                left_number = int(m2.group(1))
                l, r = bisect(left_half, m2.start(), m2.start()+len(m2.group(1)))
                left_half = l + str(int(m.group(1)) + left_number) + r
            m2 = re.search(r'^[^\d]*(\d+)', right_half)
            if m2:
                right_number = int(m2.group(1))
                l, r = bisect(right_half, m2.end()-len(m2.group(1)), m2.end())
                right_half = l + str(int(m.group(2)) + right_number) + r
            number = left_half + "0" + right_half
            break
    return number


def split(number):
    result = re.search(r'\d{2}', number)
    if result:
        x = int(result.group())
        left = floor(x / 2)
        right = ceil(x / 2)
        return number[:result.start()] + f'[{left},{right}]' + number[result.end():]
    return number

def reduce(number):
    while True:
        changed = False
        while (new_number := explode2(number)) != number:
            number = new_number
            changed = True
        if (new_number := split(number)) != number:
            number = new_number
            changed = True
        if not changed:
            break
    return number

def add(num1, num2):
    return f'[{num1},{num2}]'

def magnitude(number):
    while m := re.search(r'\[(\d+),(\d+)\]', number):
        left_number = int(m.group(1))
        right_number = int(m.group(2))
        l, r = bisect(number, m.start(), m.end())
        number = l + str(left_number * 3 + right_number * 2) + r
    return int(number)

def part1(input):
    s = None
    for i in input:
        if s is None:
            s = i
        else:
            s = reduce(add(s, i))
    return magnitude(s)

def part2(input):
    max_mag = 0
    for a in input:
        for b in input:
            if a != b:
                mag = magnitude(reduce(add(a, b)))
                if mag > max_mag:
                    max_mag = mag
    return max_mag

def main():
    input = []
    with open("18.txt") as file:
        input = [x.strip() for x in file.readlines()]
    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
