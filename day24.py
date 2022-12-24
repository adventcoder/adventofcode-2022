import framework
from math import *
from heapq import *

def solve(input):
    width, height, blizzards = parse_grid(input)
    start = (0, 0)
    end = (width - 1, height - 1)
    time = find_path(width, height, blizzards, start, end)
    yield time
    time = find_path(width, height, blizzards, end, start, time)
    time = find_path(width, height, blizzards, start, end, time)
    yield time

def parse_grid(input):
    lines = input.splitlines()
    width = len(lines[0]) - 2
    height = len(lines) - 2
    cycle_time = lcm(width, height)
    blizzards = [set() for _ in range(cycle_time)]
    for y, line in enumerate(lines[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c != '.':
                for i in range(cycle_time):
                    blizzards[i].add((x, y))
                    if c == '^':
                        y = (y - 1) % height
                    elif c == 'v':
                        y = (y + 1) % height
                    elif c == '>':
                        x = (x + 1) % width
                    elif c == '<':
                        x = (x - 1) % width
    return width, height, blizzards

def find_path(width, height, blizzards, start, end, time = 0):
    # wait for start to be clear then enter the maze
    time += 1
    while start in blizzards[time % len(blizzards)]:
        time += 1
    best_time = {}
    best_time[(start, time % len(blizzards))] = time
    queue = []
    heappush(queue, (time + estimate(start, end), time, start))
    while queue:
        _, time, pos = heappop(queue)
        if pos == end:
            # add extra minute to exit the maze
            return time + 1
        else:
            new_time = time + 1
            i = new_time % len(blizzards)
            for new_pos in neighbours(pos, width, height):
                if new_pos not in blizzards[i] and new_time < best_time.get((new_pos, i), inf):
                    best_time[(new_pos, i)] = new_time
                    heappush(queue, (new_time + estimate(new_pos, end), new_time, new_pos))

def estimate(pos, end):
    return abs(end[0] - pos[0]) + abs(end[1] - pos[1])

def neighbours(pos, width, height):
    x, y = pos
    yield x, y # wait
    if y > 0:
        yield x, y - 1
    if x > 0:
        yield x - 1, y
    if x < width - 1:
        yield x + 1, y
    if y < height - 1:
        yield x, y + 1

if __name__ == '__main__':
    framework.main()
