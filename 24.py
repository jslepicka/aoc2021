
class monad:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input_index = 0

    def set_reg(self, reg, value):
        if reg == 'w':
            self.w = value
        elif reg == 'x':
            self.x = value
        elif reg == 'y':
            self.y = value
        elif reg == 'z':
            self.z = value

    def get_val(self, x):
        if x[0] == 'w':
            return self.w
        elif x[0] == 'x':
            return self.x
        elif x[0] == 'y':
            return self.y
        elif x[0] == 'z':
            return self.z
        else:
            return int(x)

    
    def run_program(self, program, input):
        for line in program:
            print("w = %d x = %d y = %d z = %d" % (self.w, self.x, self.y, self.z))
            print(line)
            i = line.split(' ')
            ins = i[0]
            if ins == "inp":
                self.set_reg(i[1], int(input[self.input_index]))
                self.input_index += 1
            elif ins == "mul":
                self.set_reg(i[1], self.get_val(i[1]) * self.get_val(i[2]))
            elif ins == "add":
                self.set_reg(i[1], self.get_val(i[1]) + self.get_val(i[2]))
            elif ins == "mod":
                self.set_reg(i[1], self.get_val(i[1]) % self.get_val(i[2]))
            elif ins == "div":
                self.set_reg(i[1], self.get_val(i[1]) // self.get_val(i[2]))
            elif ins == "eql":
                if self.get_val(i[1]) == self.get_val(i[2]):
                    self.a = 1
                else:
                    self.a = 0
            else:
                print("invalid opcode")
                return






def part1(program):
    m = monad()
    m.run_program(program, "13579246899999")


def main():
    program = []
    with open("24.txt") as file:
        for line in [x.strip() for x in file.readlines()]:
            program.append(line)


    print("Part 1: " + str(part1(program)))
    #print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()