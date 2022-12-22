import framework
           # right, down, left, up
facings = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# TODO HARDCODED PART 2 AND DELETED PART 1

def solve(input):
    chunks = input.split('\n\n')
    grid = [list(line) for line in chunks[0].splitlines()]
    path = parse_path(chunks[1])

    transfer = {}
    for i in range(50):
        transfer[(50 + i, 0, 3)] = (0, 150 + i, 0)
        transfer[(0, 150 + i, 2)] = (50 + i, 0, 1)
    for i in range(50):
        transfer[(50, 50 - 1 - i, 2)] = (0, 100 + i, 0)
        transfer[(0, 100 + i, 2)] = (50, 50 - 1 - i, 0)
    for i in range(50):
        transfer[(50 - 1 - i, 200 - 1, 1)] = (150 - 1 - i, 0, 1)
        transfer[(150 - 1 - i, 0, 3)] = (50 - 1 - i, 200 - 1, 3)
    for i in range(50):
        transfer[(150 - 1, 50 - 1 - i, 0)] = (100 - 1, 100 + i, 2)
        transfer[(100 - 1, 100 + i, 0)] = (150 - 1, 50 - 1 - i, 2)
    for i in range(50):
        transfer[(50 - 1, 200 - 1 - i, 0)] = (100 - 1 - i, 150 - 1, 3)
        transfer[(100 - 1 - i, 150 - 1, 1)] = (50 - 1, 200 - 1 - i, 2)
    for i in range(50):
        transfer[(50, 50 + i, 2)] = (i, 100, 1)
        transfer[(i, 100, 3)] = (50, 50 + i, 0)
    for i in range(50):
        transfer[(100 - 1, 100 - 1 - i, 0)] = (150 - 1 - i, 50 - 1, 3)
        transfer[(150 - 1 - i, 50 - 1, 1)] = (100 - 1, 100 - 1 - i, 2)

    yield follow(grid, path, transfer)

def putsym(h, k, v):
    h[k] = v
    h[v] = k

def follow(grid, path, transfer):
    x = incx(grid, -1, 0, 1)
    y = 0
    dx = 1
    dy = 0
    for arg in path:
        if arg == 'L':
            dx, dy, = dy, -dx
            grid[y][x] = '>v<^'[facings.index((dx, dy))]
        elif arg == 'R':
            dx, dy = -dy, dx
            grid[y][x] = '>v<^'[facings.index((dx, dy))]
        else:
            for _ in range(arg):
                d = facings.index((dx, dy))
                if (x, y, d) in transfer:
                    next_x, next_y, next_d = transfer[(x, y, d)]
                else:
                    next_x = x + dx
                    next_y = y + dy
                    next_d = d
                print(x, y, d, next_x, next_y)
                if grid[next_y][next_x] == '#':
                    break
                x = next_x
                y = next_y
                dx, dy = facings[next_d]
                grid[y][x] = '>v<^'[facings.index((dx, dy))]
    return password(x, y, dx, dy)

def parse_path(chunk):
    tokens = chunk.replace('L', ' L ').replace('R', ' R ').split()
    return (int(token) if token.isdigit() else token for token in tokens)

def password(x, y, dx, dy):
    return 1000 * (y + 1) + 4 * (x + 1) + facings.index((dx, dy))

def incx(grid, x, y, dx):
    x = (x + dx) % len(grid[y])
    while grid[y][x] == ' ':
        x = (x + dx) % len(grid[y])
    return x

def incy(grid, x, y, dy):
    y = (y + dy) % len(grid)
    while x >= len(grid[y]) or grid[y][x] == ' ':
        y = (y + dy) % len(grid)
    return y


if __name__ == '__main__':
    example = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''
    framework.main()
