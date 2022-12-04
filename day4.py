
from utils import read_table
from dataclasses import dataclass

@dataclass
class Interval:
  min: int
  max: int

  @classmethod
  def parse(cls, s):
    return cls(*map(int, s.split('-')))

  def overlaps_all(self, other):
    return self.min <= other.min and self.max >= other.max

  def overlaps_any(self, other):
    return self.min <= other.max and self.max >= other.min

def main():
    pairs = read_table('inputs/day4.txt', [Interval.parse] * 2, separator = ',')
    print('Silver:', sum(a.overlaps_all(b) or b.overlaps_all(a) for a, b in pairs))
    print('Gold:', sum(a.overlaps_any(b) for a, b in pairs))

if __name__ == '__main__':
    main()
