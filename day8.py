import framework
from utils import parse_grid, product

def solve(input):
    grid = parse_grid(input, int)
    yield sum(visible(grid, x, y) for y in range(len(grid)) for x in range(len(grid[y])))
    yield max(scenic_score(grid, x, y) for y in range(len(grid)) for x in range(len(grid[y])))

def visible(grid, x, y):
    return any(all_viewable(line, grid[y][x]) for line in lines(grid, x, y))

def scenic_score(grid, x, y):
    return product(count_viewable(line, grid[y][x]) for line in lines(grid, x, y))

def all_viewable(line, base_height):
    return all(base_height > height for height in line)

def count_viewable(line, base_height):
    n = 0
    for height in line:
        n += 1
        if height >= base_height:
            break
    return n

def lines(grid, x, y):
    return (up(grid, x, y), left(grid, x, y), right(grid, x, y), down(grid, x, y))

def left(grid, x, y):
    return reversed(grid[y][ : x])

def right(grid, x, y):
    return grid[y][x + 1 : ]

def up(grid, x, y):
    return map(lambda row: row[x], reversed(grid[ : y]))

def down(grid, x, y):
    return map(lambda row: row[x], grid[y + 1 : ])

if __name__ == '__main__':
    framework.main()
