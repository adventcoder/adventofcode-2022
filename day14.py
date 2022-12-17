import framework
from itertools import pairwise
from contextlib import contextmanager
import gif

def solve(input, gif_path = None):
    grid = parse_grid(input)
    max_y = max(y for _, y in grid.keys())
    floor_y = max_y + 2
    start = (500, 0)
    with open_graphics(gif_path, grid, start, floor_y) as graphics:
        fill(grid, start, floor_y, max_y, graphics)
        yield sum(c == 'o' for c in grid.values())
        fill(grid, start, floor_y, floor_y, graphics)
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

def fill(grid, start, floor_y, max_y, graphics = None):
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
            if graphics is not None:
                render_grid(graphics, grid, start, floor_y, pos[0], pos[1], pos[0] + 1, pos[1] + 1)
            pos = path.pop() if path else None

@contextmanager
def open_graphics(path, grid, start, floor_y):
    if path is not None:
        x0, y0 = start[0] - floor_y, start[1]
        x1, y1 = start[0] + floor_y + 1, start[1] + floor_y
        colors = [0x000000, 0xD77A69, 0xCDAA6D]
        with gif.open_graphics(path, gif.ScreenDescriptor(x1 - x0, y1 - y0, colors)) as graphics:
            render_grid(graphics, grid, start, floor_y, x0, y0, x1, y1)
            yield graphics
    else:
        yield None

def render_grid(graphics, grid, start, floor_y, x0, y0, x1, y1):
    screen_x0, screen_y0 = start[0] - floor_y, start[1]
    image = gif.Image(x0 - screen_x0, y0 - screen_y0, x1 - x0, y1 - y0)
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = grid.get((x, y), '.')
            if c == 'o':
                image.set_pixel(x - x0, y - y0, 2)
            elif c == '#':
                image.set_pixel(x - x0, y - y0, 1)
    graphics.render(image, delay = 0.01)

if __name__ == '__main__':
    framework.main()
