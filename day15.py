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

    x, y = find_missing_beacon(sensors, Interval(0, 4000000), Interval(0, 4000000))
    yield x * 4000000 + y

def coverage(sensors, line_y):
    # Gather x intervals for each sensor
    xss = []
    for x, y, r in sensors:
        dx = r - abs(y - line_y)
        if dx >= 0:
            xss.append(Interval(x - dx, x + dx))

    # Calculate total size of all intervals taking into account overlaps
    total_size = 0
    xss.sort(key = lambda x: x.min)
    curr = xss[0]
    for xs in xss[1:]:
        if xs.min > curr.max:
            total_size += len(curr)
            curr = xs
        elif xs.max > curr.max:
            curr = Interval(curr.min, xs.max)
    total_size += len(curr)

    return total_size

def find_missing_beacon(sensors, xs, ys):
    for L1, L2 in combinations(find_line_segments(sensors), 2):
        # slopes should all be either 1 or -1
        # the beacon will be at the intersection of two perpendicular lines
        # TODO: probably don't need to enumerate line segments, could just loop directly over intersections?
        m1 = (L1[3] - L1[1]) // (L1[2] - L1[0])
        m2 = (L2[3] - L2[1]) // (L2[2] - L2[0])
        if m1 == -m2:
            # y = y1 + m1 (x - x1)
            # y = y2 - m1 (x - x2)
            #
            # x = (x1 + x2 + (y2-y1)/m1)/2
            # y = (y1 + y2 + m1 (x2-x1))/2
            #
            x = (L1[0] + L2[0] + (L2[1] - L1[1])//m1) // 2
            y = (L1[1] + L2[1] + m1*(L2[0] - L1[0])) // 2
            if x in xs and y in ys:
                return x, y

def find_line_segments(sensors):
    # Find line segments that the missing beacon could lie on.
    # These are the line segments formed between the corners of pairs of sensors that are one square apart.
    for (x1, y1, r1), (x2, y2, r2) in combinations(sensors, 2):
        if distance(x1, y1, x2, y2) == r1 + r2 + 2:
            if x2 > x1:
                x1, y1, r1, x2, y2, r2 = x2, y2, r2, x1, y1, r1
            if y2 > y1:
                if x1 > x2 - r2 - 1:
                    yield x1, y1 + r1 + 1, x2, y2 - r2 - 1 # a bottom -> b top
                elif x1 < x2 - r2 - 1:
                    yield x2 - r2 - 1, y2, x1 + r1 + 1, y1 # b left -> a right
                else:
                    assert False # TODO
            else:
                if x1 > x2 - r2 - 1:
                    yield x1, y1 - r1 - 1, x2, y2 + r2 + 1 # a top -> b bottom
                elif x1 < x2 - r2 - 1:
                    yield x2 - r2 - 1, y2, x1 + r1 + 1, y1 # b left -> a right
                else:
                    assert False # TODO

def covers(sensors, x, y):
    return any(distance(x0, y0, x, y) <= r for x0, y0, r in sensors)

def distance(x0, y0, x1, y1):
    return abs(y1 - y0) + abs(x1 - x0)

class Interval:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __len__(self):
        return self.max - self.min + 1 if self.min <= self.max else 0

    def __contains__(self, x):
        return self.min <= x <= self.max

if __name__ == '__main__':
    framework.main()
