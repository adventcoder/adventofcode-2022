import framework

#TODO: clean this

def solve(input):
    tree = parse_tree(input)
    #tree.print()

    yield sum(dir.total_size() for dir in tree.flatten() if dir.total_size() <= 100000)

    unused = 70000000 - tree.total_size()
    needed = 30000000 - unused
    yield min(dir.total_size() for dir in tree.flatten() if dir.total_size() >= needed)

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def total_size(self):
        return self.size

    def flatten(self, result = None):
        if result is None:
            result = []
        return result

    def print(self, indent = ''):
        print('%s- %s (file, size=%d)' % (indent, self.name, self.size))

class Dir:
    def __init__(self, name):
        self.name = name
        self.entries = {}
        self.size = None

    def flatten(self, result = None):
        if result is None:
            result = []
        result.append(self)
        for entry in self.entries.values():
            entry.flatten(result)
        return result

    def total_size(self):
        if self.size is None:
            self.size = sum(entry.total_size() for entry in self.entries.values())
        return self.size

    def print(self, indent = ''):
        print('%s- %s (dir)' % (indent, self.name))
        for entry in self.entries.values():
            entry.print(indent + '  ')

def parse_tree(input):
    root = Dir('/')
    path = []
    for line in input.splitlines():
        tokens = line.split()
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                if tokens[2] == '/':
                    dir = root
                    path.clear()
                elif tokens[2] == '..':
                    dir = path.pop()
                else:
                    path.append(dir)
                    dir = dir.entries[tokens[2]]
        else:
            if tokens[0] == 'dir':
                dir.entries[tokens[1]] = Dir(tokens[1])
            else:
                dir.entries[tokens[1]] = File(tokens[1], int(tokens[0]))
    return root

if __name__ == '__main__':
    framework.main()
