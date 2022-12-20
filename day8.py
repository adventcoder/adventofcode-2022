import framework
from utils import parse_grid

def solve(input):
    grid = parse_grid(input, int)
    yield part1(grid)
    yield part2(grid)

def part1(grid):
    visible = [[False] * len(row) for row in grid]
    for y, row in enumerate(grid):
        for i in find_visible(row):
            visible[y][i] = True
        for i in find_visible(reversed(row)):
            visible[y][-i - 1] = True
    for x, col in enumerate(zip(*grid)):
        for i in find_visible(col):
            visible[i][x] = True
        for i in find_visible(reversed(col)):
            visible[-i - 1][x] = True
    return sum(x for row in visible for x in row)

def find_visible(vals):
    max = None
    for i, val in enumerate(vals):
        if max is None or val > max:
            max = val
            yield i
            if max == 9:
                break

def part2(grid):
    scores = [[1] * len(row) for row in grid]
    for y, row in enumerate(grid):
        for i, d in enumerate(viewing_distances(row)):
            scores[y][i] *= d
        for i, d in enumerate(viewing_distances(row[::-1])):
            scores[y][-i - 1] *= d
    for x, col in enumerate(zip(*grid)):
        for i, d in enumerate(viewing_distances(col)):
            scores[i][x] *= d
        for i, d in enumerate(viewing_distances(col[::-1])):
            scores[-i - 1][x] *= d
    return max(score for row in scores for score in row)

def viewing_distances(vals):
    # https://en.wikipedia.org/wiki/All_nearest_smaller_values
    stack = []
    for i in range(len(vals)):
        while stack and vals[stack[-1]] < vals[i]:
            stack.pop()
        if stack:
            yield i - stack[-1]
        else:
            yield i
        stack.append(i)

if __name__ == '__main__':
    framework.main()
