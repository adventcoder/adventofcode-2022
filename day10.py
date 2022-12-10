import framework

def solve(input):
    sums = parse_sums(input)
    yield sum(signal_strength(sums, n) for n in range(20, 220 + 1, 40))
    yield '\n'.join(scan_line(sums, y, 40) for y in range(6))

def signal_strength(sums, n):
    return n * value(sums, n - 1)

def scan_line(sums, y, width):
    return ''.join('#' if x - 1 <= value(sums, x + y * width) <= x + 1 else '.' for x in range(width))

def value(sums, t):
    return sums[-1] * (t // len(sums)) + sums[t % len(sums)] + 1

def parse_sums(input):
    sums = [0]
    for line in input.splitlines():
        tokens = line.strip().split()
        if tokens[0] == 'noop':
            sums.append(sums[-1])
        elif tokens[0] == 'addx':
            sums.append(sums[-1])
            sums.append(sums[-1] + int(tokens[1]))
    return sums

if __name__ == '__main__':
    framework.main()
