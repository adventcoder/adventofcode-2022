import framework
from utils import parse_grid

def solve(input):
    grid = parse_grid(input, int)
    yield part1(grid)
    # idk how to make part 2 not super slow
    yield part2A(grid)

def part1(grid):
    visible = set()
    for y, row in enumerate(grid):
        for i in find_visible(row):
            visible.add((i, y))
        for i in find_visible(reversed(row)):
            visible.add((len(grid[y]) - i - 1, y))
    for x, col in enumerate(zip(*grid)):
        for i in find_visible(col):
            visible.add((x, i))
        for i in find_visible(reversed(col)):
            visible.add((x, len(grid) - i - 1))
    return len(visible)

def find_visible(vals):
    max = None
    for i, val in enumerate(vals):
        if max is None or val > max:
            max = val
            yield i
            if max == 9:
                break

def part2A(grid):
    best_score = 0
    for x, col in enumerate(zip(*grid)):
        for y, row in enumerate(grid):
            score = 1
            score *= viewing_distance(row[x], left(row, x))
            score *= viewing_distance(row[x], right(row, x))
            score *= viewing_distance(col[y], left(col, y))
            score *= viewing_distance(col[y], right(col, y))
            if score > best_score:
                best_score = score
    return best_score

# Slicing creates copies so try to avoid that...

def left(seq, i):
    for j in reversed(range(i)):
        yield seq[j]

def right(seq, i):
    for j in range(i + 1, len(seq)):
        yield seq[j]

def viewing_distance(head, tail):
    d = 0
    for val in tail:
        d += 1
        if val >= head:
            break
    return d

# Pythons reversed list view doesn't allow calling len or subscripting so have to pass a lambda instead

def part2B1(grid):
    scores = [[1] * len(row) for row in grid]
    for y, row in enumerate(grid):
        for i, d in enumerate(viewing_distances1(row, lambda i: i)):
            scores[y][i] *= d
        for i, d in enumerate(viewing_distances1(row, lambda i: -i - 1)):
            scores[y][-i - 1] *= d
    for x, col in enumerate(zip(*grid)):
        for i, d in enumerate(viewing_distances1(col, lambda i: i)):
            scores[i][x] *= d
        for i, d in enumerate(viewing_distances1(col, lambda i: -i - 1)):
            scores[-i - 1][x] *= d
    return max(score for row in scores for score in row)

def viewing_distances1(vals, f):
    last_index = [None] * 10
    for i in range(len(vals)):
        val = vals[f(i)]
        j = last_index[val]
        yield i if j is None else i - j
        for j in range(val + 1):
            last_index[j] = i

def part2B2(grid):
    scores = [[1] * len(row) for row in grid]
    for y, row in enumerate(grid):
        for i, d in enumerate(viewing_distances2(row, lambda i: i)):
            scores[y][i] *= d
        for i, d in enumerate(viewing_distances2(row, lambda i: -i - 1)):
            scores[y][-i - 1] *= d
    for x, col in enumerate(zip(*grid)):
        for i, d in enumerate(viewing_distances2(col, lambda i: i)):
            scores[i][x] *= d
        for i, d in enumerate(viewing_distances2(col, lambda i: -i - 1)):
            scores[-i - 1][x] *= d
    return max(score for row in scores for score in row)

def viewing_distances2(vals, f):
    distances = [0]
    for i in range(1, len(vals)):
        distance = 1
        while i - distance > 0 and vals[f(i)] > vals[f(i - distance)]:
            distance += distances[i - distance]
        distances.append(distance)
    return distances

if __name__ == '__main__':
    framework.main()
