from collections import defaultdict

def get_neighbors(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def djikstra(input):
    input = input.copy()
    unvisited_nodes = list(input.keys())
    shortest_path = {}
    previous_nodes = {}

    max_value = 1e10
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[(0, 0)] = 0
    
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        
        for n in get_neighbors(*current_min_node):
            dist = input[n]
            if dist == -1:
                continue
            v = shortest_path[current_min_node] + input[n]
            if v < shortest_path[n]:
                shortest_path[n] = v
                previous_nodes[n] = current_min_node
        unvisited_nodes.remove(current_min_node)
    
    return (previous_nodes, shortest_path)


def inc_costs(input, inc):
    input = input.copy()
    if inc == 0:
        return input
    else:
        for l in input:
            v = input[l]
            v += inc
            if v > 9:
                v -= 9
            input[l] = v
    return input
    

def part1(input):

    end_x = max(input, key=lambda p: p[0])[0]
    end_y = max(input, key=lambda p: p[1])[1]

    previous_nodes, shortest_path = djikstra(input)

    return shortest_path[(end_x, end_y)]
    


def part2(input):
    width = max(input, key=lambda p: p[0])[0] + 1
    height = max(input, key=lambda p: p[1])[1] + 1

    new_costs = defaultdict(lambda: -1)
    cache = {}

    new_map = defaultdict(lambda: -1)
    for y in range(5):
        map = inc_costs(input, y)
        for x in range(5):
            map2 = inc_costs(map, x)
            for m in map2:
                new_map[(m[0] + x*width, m[1] + y*height)] = map2[m]

    end_x = max(new_map, key=lambda p: p[0])[0]
    end_y = max(new_map, key=lambda p: p[1])[1]

    previous_nodes, shortest_path = djikstra(new_map)



    return shortest_path[(end_x, end_y)]

def main():
    input = defaultdict(lambda: -1)
    with open("15.txt") as file:
        y = 0
        for line in [x.strip() for x in file.readlines()]:
            x = 0
            for i in line:
                input[(x, y)] = int(i)
                x += 1
            y += 1


    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
