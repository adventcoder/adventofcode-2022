import framework
from utils import parse_grid
from collections import namedtuple

Pos = namedtuple('Pos', ['x', 'y'])

def solve(input):
    grid = parse_grid(input)
    start = next(positions(grid, 'S'))
    end = next(positions(grid, 'E'))
    grid[start.y][start.x] = 'a'
    grid[end.y][end.x] = 'z'
    steps = find_shortest_descents(grid, end)
    yield steps[start]
    yield min(steps[p] for p in positions(grid, 'a') if p in steps)

def positions(grid, c):
    return (Pos(x, y) for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x] == c)

def find_shortest_descents(grid, end):
    steps = { end: 0 }
    next = [end]
    while next:
        curr = next
        next = []
        for p in curr:
            for n in neighbours(p, grid):
                if n not in steps and can_step(n, p, grid):
                    steps[n] = steps[p] + 1
                    next.append(n)
    return steps

def can_step(p, q, grid):
    return ord(grid[q.y][q.x]) - ord(grid[p.y][p.x]) <= 1

def neighbours(p, grid):
    if p.x > 0:
        yield Pos(p.x - 1, p.y)
    if p.y > 0:
        yield Pos(p.x, p.y - 1)
    if p.x < len(grid[p.y]) - 1:
        yield Pos(p.x + 1, p.y)
    if p.y < len(grid) - 1:
        yield Pos(p.x, p.y + 1)

if __name__ == '__main__':
    framework.main()
