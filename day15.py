import framework
import re
from itertools import combinations

def solve(input):
    sensors = []
    beacons = set()
    for line in input.splitlines():
        x0, y0, x1, y1 = map(int, re.findall('-?\d+', line))
        sensors.append((x0, y0, distance(x0, y0, x1, y1)))
        beacons.add((x1, y1))

    yield coverage(sensors, 2000000) - sum(y == 2000000 for _, y in beacons)
    yield tuning_frequency(sensors, 4000000)

def coverage(sensors, line_y):
    xss = []
    for x, y, r in sensors:
        dx = r - abs(y - line_y)
        if dx >= 0:
            xss.append(Interval(x - dx, x + dx))
    return sum(len(xs) for xs in union(xss))

def union(xss):
    xss.sort(key = lambda x: x.min)
    curr = xss[0]
    for xs in xss[1:]:
        if xs.min > curr.max:
            yield curr
            curr = xs
        elif xs.max > curr.max:
            curr = Interval(curr.min, xs.max)
    yield curr

class Interval:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __len__(self):
        return self.max - self.min + 1 if self.min <= self.max else 0

def tuning_frequency(sensors, n):
    pos_lines = []
    neg_lines = []
    for (x1, y1, r1), (x2, y2, r2) in combinations(sensors, 2):
        if distance(x1, y1, x2, y2) == r1 + r2 + 2:
            dx = (x2 > x1) - (x2 < x1)
            dy = (y2 > y1) - (y2 < y1)
            p = (x1 + dx * (r1 + 1), y1) # or (x2 - dx * (r2+1), y2)
            (neg_lines if dx == dy else pos_lines).append(p)
    for x1, y1 in pos_lines:
        for x2, y2 in neg_lines:
            # Intersection of: y = x + y1 - x1 and y = x2 + y2 - x
            x = (x2 + x1 + y2 - y1) // 2
            y = (x2 + y1 + y2 - x1) // 2
            if 0 <= x <= n and 0 <= y <= n and not covers(sensors, x, y):
                return x * 4000000 + y

def covers(sensors, x, y):
    return any(distance(x0, y0, x, y) <= r for x0, y0, r in sensors)

def distance(x0, y0, x1, y1):
    return abs(y1 - y0) + abs(x1 - x0)

if __name__ == '__main__':
    framework.main()
