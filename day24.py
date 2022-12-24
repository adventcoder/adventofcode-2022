import framework
from math import *
from heapq import *

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
    cycle_time = lcm(len(grid) - 2, len(grid[0]) - 2)
    best_time = {}
    best_time[(start, start_time % cycle_time)] = start_time
    queue = []
    heappush(queue, (start_time + estimate(start, end), start_time, start))
    while queue:
        _, time, pos = heappop(queue)
        if pos == end:
            return time
        else:
            new_time = time + 1
            for new_pos in neighbours(grid, pos):
                if not collision(grid, new_pos, new_time):
                    key = (new_pos, new_time % cycle_time)
                    if new_time < best_time.get(key, inf):
                        best_time[key] = new_time
                        heappush(queue, (new_time + estimate(new_pos, end), new_time, new_pos))

def estimate(pos, end):
    return abs(end[0] - pos[0]) + abs(end[1] - pos[1])

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
