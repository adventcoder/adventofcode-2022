import framework
from math import *
from heapq import *
from collections import deque

def solve(input):
    grid = [list(line) for line in input.splitlines()]
    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), len(grid) - 1)
    time = find_path(grid, start, end)
    yield time
    time = find_path(grid, end, start, time)
    time = find_path(grid, start, end, time)
    yield time

def find_path(grid, start, end, start_time = 0):
    curr = set([start])
    time = start_time
    while curr:
        next = set()
        for pos in curr:
            if pos == end:
                return time
            for new_pos in neighbours(grid, pos):
                if new_pos not in next and not collision(grid, new_pos, time + 1):
                    next.add(new_pos)
        curr = next
        time += 1

def collision(grid, pos, time):
    x, y = pos
    if grid[y][x] == '#':
        return True
    if grid[y][wrapx(x - time, grid)] == '>':
        return True
    if grid[y][wrapx(x + time, grid)] == '<':
        return True
    if grid[wrapy(y - time, grid)][x] == 'v':
        return True
    if grid[wrapy(y + time, grid)][x] == '^':
        return True
    return False

def wrapx(x, grid):
    return (x - 1) % (len(grid[0]) - 2) + 1

def wrapy(y, grid):
    return (y - 1) % (len(grid) - 2) + 1

def neighbours(grid, pos):
    x, y = pos
    yield x, y # wait
    if y > 0:
        yield x, y - 1
    yield x - 1, y
    yield x + 1, y
    if y < len(grid) - 1:
        yield x, y + 1

if __name__ == '__main__':
    framework.main()
