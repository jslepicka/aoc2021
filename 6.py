state_cache = {}

def sim_state(initial_state, days):
    if initial_state in state_cache:
        return state_cache[initial_state]
    fishes = [initial_state]
    for day in range(days):
        for i in range(len(fishes)):
            fish = fishes[i]
            if fish == 0:
                fishes.append(8)
                fish = 6
            else:
                fish -= 1
            fishes[i] = fish
    fish_count = len(fishes)
    state_cache[initial_state] = fish_count
    return fish_count

def sim_state2(input, days):
    #instead of keeping track of individual fish, just keep track
    #of how many fish are in each state
    state_counts = [0] * 9
    for i in input:
        state_counts[i] += 1
    
    for _ in range(days):
        #fish that are in state 0 will spawn at the end of the day
        spawns = state_counts[0]
        #shift all the state counts down, e.g., fish in state 1 will
        #become state 0
        for i in range(9-1):
            state_counts[i] = state_counts[i+1]
        #state 8 count is the number of fish spawned this day
        state_counts[8] = spawns
        #add spawning fish to state 6 to start their cycle over
        state_counts[6] += spawns
    return sum(state_counts)

def part1(input):
    # s = 0
    # for i in input:
    #     s += sim_state(i, 80)
    # return s
    return sim_state2(input, 80)

def part2(input):
    return sim_state2(input, 256)


def main():
    input = []
    with open("6.txt") as file:
        for x in file.readlines():
            input = [int(x) for x in x.split(",")]

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
