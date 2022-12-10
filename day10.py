import framework

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
    yield ''.join(''.join(row) + '\n' for row in screen) #TODO: ocr

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
