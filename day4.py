
import framework
from utils import parse_table

def solve(input):
    pairs = parse_table(input, [Interval] * 2, separator = ',')
    yield sum(a.contains(b) or b.contains(a) for a, b in pairs)
    yield sum(a.overlaps(b) for a, b in pairs)

class Interval:
    def __init__(self, s):
        self.min, self.max = map(int, s.split('-'))

    def contains(self, other):
        return self.min <= other.min and self.max >= other.max

    def overlaps(self, other):
        return self.min <= other.max and self.max >= other.min

if __name__ == '__main__':
    framework.main()
