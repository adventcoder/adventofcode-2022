
import framework
from utils import parse_table, sgn

def solve(input):
    moves = parse_table(input, (str, int))
    yield len(set(tail_positions(moves, 2)))
    yield len(set(tail_positions(moves, 10)))

def tail_positions(moves, size):
    rope = [Knot() for _ in range(size)]
    yield rope[-1].position()
    for d, n in moves:
        for _ in range(n):
            rope[0].move(d)
            for i in range(1, len(rope)):
                rope[i].follow(rope[i - 1])
            yield rope[-1].position()

class Knot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def position(self):
        return (self.x, self.y)

    def move(self, d):
        if d == 'U':
            self.y -= 1
        elif d == 'L':
            self.x -= 1
        elif d == 'R':
            self.x += 1
        elif d == 'D':
            self.y += 1

    def follow(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        if max(abs(dx), abs(dy)) > 1:
            self.x += sgn(dx)
            self.y += sgn(dy)

if __name__ == '__main__':
    framework.main()
