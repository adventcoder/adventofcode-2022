
import framework
from utils import parse_table

def solve(input):
    pairs = parse_table(input, [Interval] * 2, separator = ',')
    yield sum(a.overlaps_all(b) or b.overlaps_all(a) for a, b in pairs)
    yield sum(a.overlaps_any(b) for a, b in pairs)

class Interval:
    def __init__(self, s):
        self.min, self.max = map(int, s.split('-'))

    def overlaps_all(self, other):
        return self.min <= other.min and self.max >= other.max

    def overlaps_any(self, other):
        return self.min <= other.max and self.max >= other.min

if __name__ == '__main__':
    framework.main()
