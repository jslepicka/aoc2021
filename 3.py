num_bits = 0

def get_counts(input):
    counts = [0] * num_bits
    for x in input:
        for i in range(num_bits):
            counts[i] += x & 1
            x >>= 1
    return counts

def get_gamma(input):
    counts = get_counts(input)
    half_input_count = len(input) / 2
    gamma = 0
    for bit, count in enumerate(counts):
        if count >= half_input_count:
            gamma |= (1 << bit)
    return gamma

def part1(input):
    gamma = get_gamma(input)
    epsilon = gamma ^ ((1 << num_bits) - 1)
    return gamma * epsilon

def get_rating(input, least_common=False):
    result = input
    bit = num_bits - 1
    gamma_xor = (1 << num_bits) - 1
    while len(result) > 1:
        gamma = get_gamma(result)
        if least_common:
            gamma ^= gamma_xor
        bitmask = 1 << bit
        check = gamma & bitmask
        result = list(filter(lambda r: r & bitmask == check, result))
        bit -= 1
    return result[0]

def part2(input):
    o2_rating = get_rating(input)
    co2_rating = get_rating(input, least_common=True)
    return o2_rating*co2_rating

def main():
    global num_bits
    input = []
    with open("3.txt") as file:
        num_bits = len(file.readline().strip())
        file.seek(0)
        input = [int(x.strip(), base=2) for x in file.readlines()]
    
    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
