from collections import defaultdict
from copy import deepcopy
def draw(input):
    width = max(input, key=lambda p: p[0])[0] + 1
    height = max(input, key=lambda p: p[1])[1] + 1
    for y in range(height):
        for x in range(width):
            e = input[(x, y)]
            if e != -1:
                print(e, end="")
        print()


def in_room(letter, x, y):
    #given a letter in x,y pos, return true if in room
    if y < 2:
        return False
    letter = letter.upper()
    i = ord(letter) - 65 + 1

def get_score(letter):
    letter = letter.upper()
    if letter == "A":
        return 1
    if letter == "B":
        return 10
    if letter == "C":
        return 100
    if letter == "D":
        return 1000
    return None

def get_neighbors(x, y):
    return [(x-1, y), (x+1, y), (x, y-1)]

def get_room_pos(letter):
    letter = letter.upper()
    if letter == "A":
        return 3
    if letter == "B":
        return 5
    if letter == "C":
        return 7
    if letter == "D":
        return 9
    return None

I = 0

def part1(burrow, amphipods):
    global I


    queue = []
    queue.append((burrow, amphipods))
    while queue:
        burrow, amphipods = queue.pop()
        I += 1
        if I % 10000 == 0:
            draw(burrow)
            print(len(queue))
        for pod in amphipods:
            pod_state, x, y, energy, visited = amphipods[pod]
            if (x, y) in visited:
                continue
            #visited.append((x,y))
            v = list(visited)
            v.append((x,y))
            visited = tuple(v)
            #if pod is in room, stop
            if pod_state == 2:
                #need to check for end_state here
                done = True
                for p in amphipods:
                    if amphipods[p][0] != 2:
                        done = False
                if done:
                    draw(burrow)
                    x = 1
                    return
                #continue
            elif pod_state == 0: #moving into/in hallway
                decisions = [(-1, -1)]
                decisions.extend(get_neighbors(x,y))
                for n in decisions:
                    next_burrow = burrow.copy()
                    next_state = deepcopy(amphipods)
                    if n[0] == -1: #if stop decision
                        if y == 1: #and in hallway
                            next_state[pod] = [1, x, y, energy, ()]
                            #part1(next_burrow, next_state)
                            queue.append((next_burrow, next_state))
                    elif burrow[n] != ".": #else if the next position would stop us
                            next_state[pod] = [1, x, y, energy, ()]
                            #part1(next_burrow, next_state)
                            queue.append((next_burrow, next_state))
                    else:
                        #don't move south from hallway
                        if y == 1 and n[1] > 1:
                            continue
                        next_burrow[n] = pod
                        next_burrow[x, y] = "."
                        next_state[pod] = [pod_state, *n, get_score(pod), visited]
                        #part1(next_burrow, next_state)
                        queue.append((next_burrow, next_state))

            elif pod_state == 1: #moving back into room
                #check if letter is over correct room
                next_burrow = burrow.copy()
                next_state = deepcopy(amphipods)
                room_x = get_room_pos(pod)
                if x == room_x:
                    #if room y 3 char differs just skip
                    #otherwise drop into room
                    # if y == 1 and burrow[(x, y+2)].upper() != pod.upper():
                    #     j = 1
                    # elif burrow[(x, y+1)] == ".":
                    #     #draw(burrow)
                    #     #move south
                    #     next_burrow[(x, y)] = "."
                    #     next_burrow[(x, y+1)] = pod
                    #     next_state[pod] = [pod_state, x, y+1, get_score(pod), visited]
                    #     queue.append((next_burrow, next_state))
                    if burrow[(x, 3)] == ".":
                        next_burrow[(x, y)] = "."
                        next_burrow[(x, 3)] = pod
                        next_state[pod] = [2, x, 3, get_score(pod), visited]
                        queue.append((next_burrow, next_state))
                    elif burrow[(x, 3)].isalpha() and burrow[(x, 3)].upper() != pod.upper():
                        j = 1 #skip
                    elif burrow[(x,2)] == ".":
                        next_burrow[(x, y)] = "."
                        next_burrow[(x, 2)] = pod
                        next_state[pod] = [2, x, 2, get_score(pod), visited]
                        queue.append((next_burrow, next_state))

                else:
                    if x < room_x and burrow[(x+1, y)] == ".":
                        next_burrow[(x, y)] = "."
                        next_burrow[(x+1, y)] = pod
                        next_state[pod] = [pod_state, x+1, y, get_score(pod), visited]
                        queue.append((next_burrow, next_state))
                    elif x > room_x and burrow[(x-1, y)] == ".":
                        next_burrow[(x, y)] = "."
                        next_burrow[(x-1, y)] = pod
                        next_state[pod] = [pod_state, x-1, y, get_score(pod), visited]
                        queue.append((next_burrow, next_state))
                

            



    return None

def part2(input):
    return None

def main():
    burrow = defaultdict(lambda: " ")
    amphipods = {}
    with open("23.txt") as file:
        y = 0
        letter_counts = [0] * 4
        for line in [x.replace("\n", "") for x in file.readlines()]:
            x = 0
            for i in line:
                if i.isalpha():
                    j = ord(i) - 65
                    if letter_counts[j] == 0:
                        i = chr(j + 65)
                        letter_counts[j] += 1
                    else:
                        i = chr(j + 97)
                    amphipods[i] = [0, x, y, 0, ()]
                burrow[(x, y)] = i
                x += 1
            y += 1

    draw(burrow)
    print(amphipods)

    print("Part 1: " + str(part1(burrow, amphipods)))
    print("Part 2: " + str(part2(burrow)))

if __name__ == "__main__":
    main()
