import framework
import re

facings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
R, D, L, U = range(len(facings))

tile_size = 50

# TODO: not hardcode this
net = {
    (1, 0, L): (0, 2, R),
    (1, 0, U): (0, 3, R),
    (2, 0, R): (1, 2, L),
    (2, 0, D): (1, 1, L),
    (2, 0, U): (0, 3, U),
    (1, 1, R): (2, 0, U),
    (1, 1, L): (0, 2, D),
    (0, 2, L): (1, 0, R),
    (0, 2, U): (1, 1, R),
    (1, 2, R): (2, 0, L),
    (1, 2, D): (0, 3, L),
    (0, 3, R): (1, 2, U),
    (0, 3, D): (2, 0, D),
    (0, 3, L): (1, 0, D)
}

def solve(input):
    chunks = input.split('\n\n')
    grid = [list(line) for line in chunks[0].splitlines()]
    path = [int(token) if token.isdigit() else token for token in re.findall(r'\d+|L|R', chunks[1].strip())]
    yield password(grid, path, wrap1)
    yield password(grid, path, wrap2)

def password(grid, path, wrap):
    x = grid[0].index('.')
    y = 0
    d = 0
    for arg in path:
        if arg == 'L':
            d = (d - 1) % len(facings)
        elif arg == 'R':
            d = (d + 1) % len(facings)
        else:
            for _ in range(arg):
                dx, dy = facings[d]
                next_x = x + dx
                next_y = y + dy
                next_d = d
                if not in_bounds(grid, next_x, next_y):
                    # print(f"pre wrap: {x} {y} {d}")
                    next_x, next_y, next_d = wrap(grid, x, y, d)
                    # print(f"post wrap: {next_x} {next_y} {next_d}")
                if grid[next_y][next_x] == '#':
                    break
                x, y, d = next_x, next_y, next_d
    return 1000 * (y + 1) + 4 * (x + 1) + d

def in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y]) and grid[y][x] != ' '

def wrap1(grid, x, y, d):
    dx, dy = facings[d]
    x = (x + dx) % len(grid[0])
    y = (y + dy) % len(grid)
    while not in_bounds(grid, x, y):
        x = (x + dx * tile_size) % len(grid[0])
        y = (y + dy * tile_size) % len(grid)
    return x, y, d

def wrap2(grid, x, y, d):
    tile_x, x = divmod(x, tile_size)
    tile_y, y = divmod(y, tile_size)
    new_tile_x, new_tile_y, new_d = net[(tile_x, tile_y, d)]

    if d == R:
        assert x == tile_size - 1
        i = y
    elif d == D:
        assert y == tile_size - 1
        i = tile_size - 1 - x
    elif d == L:
        assert x == 0
        i = tile_size - 1 - y
    elif d == U:
        assert y == 0
        i = x

    if new_d == R:
        new_x = 0
        new_y = i
    elif new_d == D:
        new_x = tile_size - 1 - i
        new_y = 0
    elif new_d == L:
        new_x = tile_size - 1
        new_y = tile_size - 1 - i
    elif new_d == U:
        new_x = i
        new_y = tile_size - 1

    return new_tile_x * tile_size + new_x, new_tile_y * tile_size + new_y, new_d

if __name__ == '__main__':
    framework.main()
