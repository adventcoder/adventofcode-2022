import framework
import re

def solve(input):
    yield format_snafu(sum(map(parse_snafu, input.splitlines())))

def parse_snafu(s):
    n = 0
    for c in s.strip():
        if c == '=':
            d = -2
        elif c == '-':
            d = -1
        else:
            d = int(c)
        n = 5 * n + d
    return n

def format_snafu(n):
    cs = []
    while n > 0:
        d = (n + 2) % 5 - 2
        if d == -2:
            cs.append('=')
        elif d == -1:
            cs.append('-')
        else:
            cs.append(str(d))
        n = (n - d) // 5
    return ''.join(reversed(cs))

if __name__ == '__main__':
    framework.main()
