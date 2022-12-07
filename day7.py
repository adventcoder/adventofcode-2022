import framework

def solve(input):
    sizes = parse_total_sizes(input)
    yield sum(size for size in sizes if size <= 100000)
    unused = 70000000 - sizes[0]
    needed = 30000000 - unused
    yield min(size for size in sizes if size >= needed)

def parse_total_sizes(input):
    sizes = []
    path = []
    for line in input.splitlines():
        tokens = line.split()
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                if tokens[2] == '..':
                    size = sizes[path.pop()]
                    sizes[path[-1]] += size
                else:
                    # we assume each dir just shows up once in the input, so can use just it's index instead of the dirname
                    path.append(len(sizes))
                    sizes.append(0)
        elif tokens[0] != 'dir':
            sizes[path[-1]] += int(tokens[0])
    while len(path) > 1:
        size = sizes[path.pop()]
        sizes[path[-1]] += size
    return sizes

if __name__ == '__main__':
    framework.main()
