from enum import Enum

class bitreader:
    def __init__(self, bitstream):
        self.bitstream = bitstream.copy()
    
    def get_bits(self, num_bits):
        ret = 0
        for i in range(num_bits):
            ret <<= 1

            ret |= self.bitstream.pop(0)
        return ret
    def align(self):
        discard_count = len(self.bitstream) % 4
        for _ in range(discard_count):
            self.bitstream.pop(0)
    def has_bits(self):
        return len(self.bitstream) > 0

def parse1(br):
    ver = br.get_bits(3)
    print("version: ", ver)
    id = br.get_bits(3)
    bits_read = 6

    literal = 0
    i = 0
    if id == 4:
        #literal
        while True:
            literal <<= 4
            l = br.get_bits(5)
            bits_read += 5
            literal |= l & 15
            if not l & 16:
                break
        print("literal ", literal)
    else:
        length_type = br.get_bits(1)
        bits_read += 1
        if length_type == 0:
            total_length = br.get_bits(15)
            print("total length: ", total_length)
            bits_read += 15
            i = 0
            while i < total_length:
                ii, tv = parse1(br)
                i += ii
                print("length parse returned ", ii, tv)
                ver += tv
            bits_read += i
        else:
            sub_packets = br.get_bits(11)
            print("sub packets: ", sub_packets)
            bits_read += 11
            c = 0
            i = 0
            while c < sub_packets:
                ii, tv = parse1(br)
                c += 1
                i += ii
                print("sub packet parse returned ", ii, tv)
                ver += tv
            bits_read += i

    return bits_read, ver


def parse2(br):
    answer = 0
    ver = br.get_bits(3)
    print("version: ", ver)
    id = br.get_bits(3)
    bits_read = 6
    vals = []
    literal = 0
    i = 0
    if id == 4:
        #literal
        while True:
            literal <<= 4
            l = br.get_bits(5)
            bits_read += 5
            literal |= l & 15
            if not l & 16:
                break
        print("literal ", literal)
    else:
        length_type = br.get_bits(1)
        bits_read += 1
        if length_type == 0:
            total_length = br.get_bits(15)
            print("total length: ", total_length)
            bits_read += 15
            i = 0
            while i < total_length:
                ii, tv = parse2(br)
                i += ii
                print("length parse returned ", ii, tv)
                vals.append(tv)
            bits_read += i
        else:
            sub_packets = br.get_bits(11)
            print("sub packets: ", sub_packets)
            bits_read += 11
            c = 0
            i = 0
            while c < sub_packets:
                ii, tv = parse2(br)
                c += 1
                i += ii
                print("sub packet parse returned ", ii, tv)
                vals.append(tv)
            bits_read += i
        if id == 0: #sum
            literal = sum(vals)
        elif id == 1: #product
            a = 1
            for v in (vals):
                a *= v
            literal = a
        elif id == 2: #min
            literal = min(vals)
        elif id == 3: #max
            literal = max(vals)
        elif id == 5: #gt
            literal = int(vals[0] > vals[1])
        elif id == 6: #lt
            literal = int(vals[0] < vals[1])
        elif id == 7: #equal
            literal = int(vals[0] == vals[1])


    return bits_read, literal

def part1(input):
    br = bitreader(input)
    _, v = parse1(br)
  
    return v

def part2(input):
    br = bitreader(input)
    _, v = parse2(br)
    return v

def main():
    s = ""
    input = []
    with open("16.txt") as file:
        s = file.readline().strip()
    
    for i in range(len(s)//2):
        x = int(s[i*2:i*2+2], base=16)
        b = bin(x).split("0b")[1]
        if len(b) < 8:
            b = "0" * (8 - len(b)) + b
        for bit in b:
            input.append(int(bit))

    print(input)

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
