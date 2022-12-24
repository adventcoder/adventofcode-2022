import framework
from collections import deque
from math import lcm

def solve(input):
    grid = [list(line) for line in input.splitlines()]

    blizzards = parse_blizzards(grid)
    start_y = 0
    start_x = grid[start_y].index('.')
    end_y = len(grid) - 1
    end_x = grid[end_y].index('.')

    time = find_path(grid, blizzards, start_x, start_y, end_x, end_y, 0)
    yield time
    time = find_path(grid, blizzards, end_x, end_y, start_x, start_y, time)
    time = find_path(grid, blizzards, start_x, start_y, end_x, end_y, time)
    yield time

def parse_blizzards(grid):
    cycle_time = lcm(len(grid) - 2, len(grid[0]) - 2)
    blizzards = [set() for _ in range(cycle_time)]
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            for z in range(cycle_time):
                if grid[y][x] == '^':
                    blizzards[z].add((x, (y - 1 - z) % (len(grid) - 2) + 1))
                elif grid[y][x] == 'v':
                    blizzards[z].add((x, (y - 1 + z) % (len(grid) - 2) + 1))
                elif grid[y][x] == '>':
                    blizzards[z].add(((x - 1 + z) % (len(grid[y]) - 2) + 1, y))
                elif grid[y][x] == '<':
                    blizzards[z].add(((x - 1 - z) % (len(grid[y]) - 2) + 1, y))
    return blizzards

def find_path(grid, blizzards, start_x, start_y, end_x, end_y, start_time):
    start = (start_x, start_y, start_time % len(blizzards))
    queue = deque([start])
    time = { start: start_time }
    while queue:
        x, y, z = queue.popleft()
        if x == end_x and y == end_y:
            return time[(x, y, z)]
        else:
            next_time = time[(x, y, z)] + 1
            next_z = next_time % len(blizzards)
            for next_x, next_y in neighbours(grid, x, y):
                next = (next_x, next_y, next_z)
                if next not in time and grid[next_y][next_x] != '#' and not (next_x, next_y) in blizzards[next_z]:
                    time[next] = next_time
                    queue.append(next)

def neighbours(grid, x, y):
    yield x, y # wait
    if y > 0:
        yield x, y - 1
    yield x - 1, y
    yield x + 1, y
    if y < len(grid) - 1:
        yield x, y + 1

if __name__ == '__main__':
    framework.main()
