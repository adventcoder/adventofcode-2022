import framework
import re

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
    #TODO: this is pretty slow!
    stack = [(xs, ys)]
    while stack:
        xs, ys = stack.pop()
        if len(xs) * len(ys) == 1:
            return xs.min, ys.min
        else:
            for new_xs in xs.split():
                for new_ys in ys.split():
                    if not any(completely_covers(sensor, new_xs, new_ys) for sensor in sensors):
                        stack.append((new_xs, new_ys))

def completely_covers(sensor, xs, ys):
    x0, y0, r = sensor
    return all(distance(x0, y0, x1, y1) <= r for x1 in (xs.min, xs.max) for y1 in (ys.min, ys.max))

def distance(x0, y0, x1, y1):
    return abs(y1 - y0) + abs(x1 - x0)

class Interval:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __len__(self):
        return self.max - self.min + 1 if self.min <= self.max else 0

    def split(self):
        mid = self.min + (self.max - self.min) // 2
        if self.min <= mid:
            yield Interval(self.min, mid)
        if mid < self.max:
            yield Interval(mid + 1, self.max)

if __name__ == '__main__':
    framework.main()
