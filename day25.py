import framework

def solve(input):
    yield format_snafu(sum(map(parse_snafu, input.splitlines())))

def parse_snafu(s):
    n = 0
    for c in s.strip():
        n = n * 5 + ('=-012'.index(c) - 2)
    return n

def format_snafu(n):
    cs = []
    while n != 0:
        d = (n + 2) % 5 - 2
        cs.append('=-012'[d + 2])
        n = (n - d) // 5
    return ''.join(reversed(cs))

if __name__ == '__main__':
    framework.main()
