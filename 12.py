from collections import defaultdict

def findpaths(input, node, dest, pathlist, *, multinode=None, multicount=2, path=None, visited=None):
    if path is None:
        path = (node,)
    if visited is None:
        visited = defaultdict(lambda: 0)
    if node[0].islower():
        if multinode is not None and node == multinode:
            multicount -= 1
            if multicount == 0:
                visited[node] = 1
        elif node != dest:
            visited[node] = 1
    if node == dest:
        pathlist.add(path)
        return
    for n in input[node]:
        if not visited[n]:
            path += (n,)
            findpaths(input, n, dest, pathlist, multinode=multinode, multicount=multicount, path=path, visited=visited)
            path = path[:-1]
    visited[node] = 0

def part1(input):
    pathlist = set()
    findpaths(input, "start", "end", pathlist)
    return len(pathlist)

def part2(input):
    smallcaves = []
    pathlist = set()
    for i in input:
        if i[0].islower() and i != "start" and i != "end":
            smallcaves.append(i)
    for cave in smallcaves:
        findpaths(input, "start", "end", pathlist, multinode=cave)
    return len(pathlist)

def main():
    input = defaultdict(list)
    with open("12.txt") as file:
        for line in file.readlines():
            a, b = line.strip().split("-")
            input[a].append(b)
            input[b].append(a)

    print("Part 1: " + str(part1(input)))
    print("Part 2: " + str(part2(input)))

if __name__ == "__main__":
    main()
