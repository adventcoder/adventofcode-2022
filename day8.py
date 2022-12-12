import framework
from utils import parse_grid
from math import prod

def solve(input):
    grid = parse_grid(input, int)
    yield sum(visible(origin, rays) for origin, rays in view_points(grid))
    yield max(scenic_score(origin, rays) for origin, rays in view_points(grid))

def view_points(grid):
    for x, col in enumerate(zip(*grid)):
        for y, row in enumerate(grid):
            yield grid[y][x], (reversed(row[ : x]), row[x + 1 : ], reversed(col[ : y]), col[y + 1 : ])

def visible(origin, rays):
    return any(all(origin > height for height in ray) for ray in rays)

def scenic_score(origin, rays):
    return prod(viewing_distance(origin, ray) for ray in rays)

def viewing_distance(origin, ray):
    n = 0
    for height in ray:
        n += 1
        if origin <= height:
            break
    return n

if __name__ == '__main__':
    framework.main()
