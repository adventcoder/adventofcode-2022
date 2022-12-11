import framework
from utils import ocr
from fonts import letters4x6

def solve(input):
    values = cpu(input)
    cycle = 0
    total_signal = 0
    screen = [['.' for _ in range(40)] for _ in range(6)]
    for y in range(len(screen)):
        for x in range(len(screen[y])):
            value = next(values)
            cycle += 1
            if (cycle - 20) % 40 == 0:
                total_signal += value * cycle
            if value - 1 <= x <= value + 1:
                screen[y][x] = '#'
    yield total_signal
    yield ocr(screen, letters4x6)

def cpu(input):
    x = 1
    for line in input.splitlines():
        tokens = line.split()
        if tokens[0] == 'noop':
            yield x
        elif tokens[0] == 'addx':
            yield x
            yield x
            x += int(tokens[1])

if __name__ == '__main__':
    framework.main()
