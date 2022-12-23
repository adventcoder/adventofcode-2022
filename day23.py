import framework

ALL = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
NORTH = [(-1, -1), ( 0, -1), ( 1, -1)]
SOUTH = [(-1,  1), ( 0,  1), ( 1,  1)]
WEST = [(-1, -1), (-1,  0), (-1,  1)]
EAST = [( 1, -1), ( 1,  0), ( 1,  1)]

# TODO: another one that's super slow
def solve(input):
    yield part1(input)
    yield part2(input)

def part1(input, rounds = 10, verbose = False):
    grid = parse_grid(input)
    dirs = [NORTH, SOUTH, WEST, EAST]
    if verbose:
        print('== Initial State ==')
        print_grid(grid)
    for i in range(rounds):
        apply_moves(grid, propose_moves(grid, dirs))
        dirs.append(dirs.pop(0))
        if verbose:
            print()
            print(f'== End of round {i + 1} ==')
            print_grid(grid)
    (x0, y0), (x1, y1) = bounding_box(grid)
    return (x1 - x0) * (y1 - y0) - len(grid)

def part2(input):
    grid = parse_grid(input)
    dirs = [NORTH, SOUTH, WEST, EAST]
    round = 1
    moves = propose_moves(grid, dirs)
    while moves:
        apply_moves(grid, moves)
        round += 1
        dirs.append(dirs.pop(0))
        moves = propose_moves(grid, dirs)
    return round

def parse_grid(input):
    grid = set()
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                grid.add((x, y))
    return grid

def print_grid(grid):
    (x0, y0), (x1, y1) = bounding_box(grid)
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            row.append('#' if (x, y) in grid else '.')
        print(''.join(row))

def bounding_box(grid):
    min_x = min(x for x, _ in grid)
    max_x = max(x for x, _ in grid)
    min_y = min(y for _, y in grid)
    max_y = max(y for _, y in grid)
    return (min_x, min_y), (max_x + 1, max_y + 1)

def propose_moves(grid, dirs):
    moves = {}
    for p in grid:
        x, y = p
        if any((x + dx, y + dy) in grid for dx, dy in ALL):
            for dir in dirs:
                if not any((x + dx, y + dy) in grid for dx, dy in dir):
                    dx, dy = dir[1]
                    new_p = (x + dx, y + dy)
                    if new_p in moves:
                        # two elves trying to move to the same spot cancel out
                        # it's not possible for more than two elves to propose the same spot
                        del moves[new_p]
                    else:
                        moves[new_p] = p
                    break
    return moves

def apply_moves(grid, moves):
    for new_p, p in moves.items():
        grid.remove(p)
        grid.add(new_p)

if __name__ == '__main__':
    framework.main()
