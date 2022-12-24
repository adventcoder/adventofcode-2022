import framework
from math import *

def solve(input):
    grid = input.splitlines()
    grids = superpositions(grid)
    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), len(grid) - 1)
    time = find_path(grids, start, end)
    yield time
    time = find_path(grids, end, start, time)
    time = find_path(grids, start, end, time)
    yield time

def superpositions(grid):
    inner_width = len(grid[0]) - 2
    inner_height = len(grid) - 2
    depth = lcm(inner_width, inner_height)
    grids = [[['.'] * len(row) for row in grid] for _ in range(depth)]
    for i in range(depth):
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == '#':
                    grids[i][y][x] = '#'
                elif c == '>':
                    grids[i][y][(x - 1 + i) % inner_width + 1] = '#'
                elif c == '<':
                    grids[i][y][(x - 1 - i) % inner_width + 1] = '#'
                elif c == 'v':
                    grids[i][(y - 1 + i) % inner_height + 1][x] = '#'
                elif c == '^':
                    grids[i][(y - 1 - i) % inner_height + 1][x] = '#'
    return grids

def find_path(grids, start, end, start_time = 0):
    curr = set([start])
    time = start_time
    while curr:
        next = set()
        for pos in curr:
            if pos == end:
                return time
            i = (time + 1) % len(grids)
            for new_pos in neighbours(pos, len(grids[i])):
                if grids[i][new_pos[1]][new_pos[0]] == '.':
                    next.add(new_pos)
        curr = next
        time += 1

def neighbours(pos, height):
    x, y = pos
    yield x, y # wait
    if y > 0:
        yield x, y - 1
    yield x - 1, y
    yield x + 1, y
    if y < height - 1:
        yield x, y + 1

if __name__ == '__main__':
    framework.main()
