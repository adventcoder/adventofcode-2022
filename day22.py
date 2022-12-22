import framework
import re

facings = [(1, 0), (0, 1), (-1, 0), (0, -1)]

tile_width = 50
tile_height = 50

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
                    next_x, next_y, next_d = wrap(grid, x, y, d)
                if grid[next_y][next_x] == '#':
                    break
                x, y, d = next_x, next_y, next_d
    return 1000 * (y + 1) + 4 * (x + 1) + d

def in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y]) and grid[y][x] != ' '

def wrap1(grid, x, y, d):
    dx, dy = facings[d]
    # loop over tiles instead of individual pixels
    tile_xcount = len(grid[y]) // tile_width
    tile_ycount = len(grid) // tile_height
    x = (x + dx) % len(grid[y])
    y = (y + dy) % len(grid)
    tile_x, ox = divmod(x, tile_width)
    tile_y, oy = divmod(y, tile_height)
    while not in_bounds(grid, tile_x * tile_width, tile_y * tile_height):
        tile_x = (tile_x + dx) % tile_xcount
        tile_y = (tile_y + dy) % tile_ycount
    return tile_x * tile_width + ox, tile_y * tile_height + oy, d

def wrap2(grid, x, y, d):
    # TODO: not hardcode this (never going to happen)
    tile_x, ox = divmod(x, tile_width)
    tile_y, oy = divmod(y, tile_height)
    if tile_x == 1 and tile_y == 0:
        if d == 2:
            return (0, 3 * tile_height - 1 - oy, 0)
        elif d == 3:
            return (0, 3 * tile_height + ox, 0)
    elif tile_x == 2 and tile_y == 0:
        if d == 0:
            return (2 * tile_width - 1, 3 * tile_height - 1 - oy, 2)
        elif d == 1:
            return (2 * tile_width - 1, tile_height + ox, 2)
        elif d == 3:
            return (ox, 4 * tile_height - 1, 3)
    elif tile_x == 1 and tile_y == 1:
        if d == 0:
            return (2 * tile_width + oy, tile_height - 1, 3)
        elif d == 2:
            return (oy, 2 * tile_height, 1)
    elif tile_x == 0 and tile_y == 2:
        if d == 2:
            return (tile_width, tile_height - 1 - oy, 0)
        elif d == 3:
            return (tile_width, tile_height + ox, 0)
    elif tile_x == 1 and tile_y == 2:
        if d == 0:
            return (3 * tile_width - 1, tile_height - 1 - oy, 2)
        elif d == 1:
            return (tile_width - 1, 3 * tile_height + ox, 2)
    elif tile_x == 0 and tile_y == 3:
        if d == 0:
            return (tile_width + oy, 3 * tile_height - 1, 3)
        elif d == 1:
            return (2 * tile_width + ox, 0, 1)
        elif d == 2:
            return (tile_width + oy, 0, 1)
    assert False

if __name__ == '__main__':
    framework.main()
