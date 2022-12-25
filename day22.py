import framework
import re

facings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
R, D, L, U = range(len(facings))

tile_size = 50

def solve(input):
    chunks = input.split('\n\n')
    grid = [list(line) for line in chunks[0].splitlines()]
    path = [int(token) if token.isdigit() else token for token in re.findall(r'\d+|L|R', chunks[1].strip())]
    yield password(grid, path, find_edges1(grid))
    yield password(grid, path, find_edges2(grid))

def password(grid, path, edges):
    x = grid[0].index('.')
    y = 0
    d = 0
    for n in path:
        if n == 'L':
            d = (d - 1) % len(facings)
        elif n == 'R':
            d = (d + 1) % len(facings)
        else:
            for _ in range(n):
                dx, dy = facings[d]
                next_x = x + dx
                next_y = y + dy
                next_d = d
                if not in_bounds(grid, next_x, next_y):
                    # print(f"pre wrap: {x} {y} {d}")
                    next_x, next_y, next_d = wrap(x, y, d, edges)
                    # print(f"post wrap: {next_x} {next_y} {next_d}")
                if grid[next_y][next_x] == '#':
                    break
                x, y, d = next_x, next_y, next_d
    return 1000 * (y + 1) + 4 * (x + 1) + d

def in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y]) and grid[y][x] != ' '

def wrap(x, y, d, edges):
    tile_x, x = divmod(x, tile_size)
    tile_y, y = divmod(y, tile_size)
    new_tile_x, new_tile_y, new_d = edges[(tile_x, tile_y, d)]

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

def find_edges1(grid):
    x_tiles = max(map(len, grid)) // tile_size
    y_tiles = len(grid) // tile_size
    edges = {}
    for y in range(y_tiles):
        x_min = next(x for x in range(x_tiles) if in_bounds(grid, x * tile_size, y * tile_size))
        x_max = next(x for x in reversed(range(x_tiles)) if in_bounds(grid, x * tile_size, y * tile_size))
        edges[(x_min, y, L)] = (x_max, y, L)
        edges[(x_max, y, R)] = (x_min, y, R)
    for x in range(x_tiles):
        y_min = next(y for y in range(y_tiles) if in_bounds(grid, x * tile_size, y * tile_size))
        y_max = next(y for y in reversed(range(y_tiles)) if in_bounds(grid, x * tile_size, y * tile_size))
        edges[(x, y_min, U)] = (x, y_max, U)
        edges[(x, y_max, D)] = (x, y_min, D)
    return edges

def find_edges2(grid):
    net = set()
    y_tiles = len(grid) // tile_size
    for y in range(y_tiles):
        x_tiles = len(grid[y * tile_size]) // tile_size
        for x in range(x_tiles):
            if grid[y * tile_size][x * tile_size] != ' ':
                net.add((x, y))

    faces = {}
    edges = {}

    def traverse(cube_pos, cube_dir, net_pos):
        if cube_pos not in faces:
            faces[cube_pos] = (net_pos, cube_dir)
            for d, facing in enumerate(facings):
                new_cube_pos, new_cube_dir = cube_translate(cube_pos, cube_dir, d)
                new_net_pos = (net_pos[0] + facing[0], net_pos[1] + facing[1])
                if new_net_pos in net:
                    # tiles are connected in the net
                    traverse(new_cube_pos, new_cube_dir, new_net_pos)
                elif new_cube_pos in faces:
                    # tiles weren't connected in the net, but they are on the cube, so we can add an edge
                    new_net_pos, new_cube_dir = faces[new_cube_pos]
                    d_inv = inverse_cube_translate(cube_pos, new_cube_pos, new_cube_dir)
                    edges[(*net_pos, d)] = (*new_net_pos, reverse_dir(d_inv))
                    edges[(*new_net_pos, d_inv)] = (*net_pos, reverse_dir(d))
    traverse((0, 1, 0), (1, 0, 0), next(iter(net)))

    return edges

def cube_translate(pos, dir, d):
    if d == R:
        return dir, negate(pos)
    elif d == D:
        return cross(dir, pos), dir
    elif d == L:
        return negate(dir), pos
    elif d == U:
        return cross(pos, dir), dir

def inverse_cube_translate(pos, old_pos, old_dir):
    if old_dir == pos:
        return R
    elif cross(old_dir, old_pos) == pos:
        return D
    elif negate(old_dir) == pos:
        return L
    elif cross(old_pos, old_dir) == pos:
        return U

def cross(a, b):
    return a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]

def negate(xs):
    return tuple(-x for x in xs)

def reverse_dir(d):
    return (d + 2) % len(facings)

if __name__ == '__main__':
    framework.main()
