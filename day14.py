import framework
from itertools import pairwise
import gif

def solve(input):
    grid = parse_grid(input)
    max_y = max(y for _, y in grid.keys())
    floor_y = max_y + 2
    start = (500, 0)
    # with gif.open_graphics('day14.gif', gif.ScreenDescriptor(2 * floor_y + 1, floor_y)) as graphics:
    #     render_grid(graphics, grid, start, floor_y)
    fill(grid, start, floor_y, max_y)
    yield sum(c == 'o' for c in grid.values())
    fill(grid, start, floor_y, floor_y)
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

def render_grid(graphics, grid, start, floor_y):
    x0, y0 = start[0] - floor_y, start[1]
    x1, y1 = start[0] + floor_y + 1, start[1] + floor_y
    image = gif.Image(0, 0, x1 - x0, y1 - y0)
    image.colors = [0x000000, 0xCCCCCC, 0xFFFFFF]
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = grid.get((x, y), '.')
            if c == 'o':
                image.set_pixel(x - x0, y - y0, 2)
            elif c == '#':
                image.set_pixel(x - x0, y - y0, 1)
    graphics.render(image, delay = 1)

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
