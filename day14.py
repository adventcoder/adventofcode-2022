import framework
from itertools import pairwise

def solve(input):
    grid = parse_grid(input)
    max_y = max(y for _, y in grid.keys())
    floor_y = max_y + 2
    fill(grid, (500, 0), floor_y, max_y)
    yield sum(c == 'o' for c in grid.values())
    fill(grid, (500, 0), floor_y, floor_y)
    yield sum(c == 'o' for c in grid.values())

def parse_grid(input):
    grid = {}
    for line in input.splitlines():
        coords = [tuple(int(s) for s in coords.split(',')) for coords in line.split('->')]
        for (x0, y0), (x1, y1) in pairwise(coords):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    grid[(x, y)] = '#'
    return grid

def fill(grid, start, floor_y, max_y):
    path = []
    pos = start
    while pos and pos[1] < max_y:
        for dx in (0, -1, 1):
            new_pos = (pos[0] + dx, pos[1] + 1)
            if new_pos not in grid and new_pos[1] < floor_y:
                path.append(pos)
                pos = new_pos
                break
        else:
            grid[pos] = 'o'
            pos = path.pop() if path else None

if __name__ == '__main__':
    framework.main()
