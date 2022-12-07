import framework

def solve(input):
    sizes = parse_dirs(input)
    yield sum(size for size in sizes.values() if size <= 100000)
    unused = 70000000 - sizes['/']
    needed = 30000000 - unused
    yield min(size for size in sizes.values() if size >= needed)

def parse_dirs(input):
    sizes = {}
    stack = []
    for line in input.splitlines():
        tokens = line.split()
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                if tokens[2] == '..':
                    child_size = sizes[stack.pop()]
                    sizes[stack[-1]] += child_size
                else:
                    path = (stack[-1], tokens[2]) if stack else tokens[2]
                    stack.append(path)
                    sizes[path] = 0
        elif tokens[0] != 'dir':
            sizes[stack[-1]] += int(tokens[0])
    while len(stack) > 1:
        child_size = sizes[stack.pop()]
        sizes[stack[-1]] += child_size
    return sizes

if __name__ == '__main__':
    framework.main()
