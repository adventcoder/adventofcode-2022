import sys

def main():
    print_input(generate_values(sys.stdin.read()))

def generate_values(screen):
    for line in screen.splitlines():
        assert len(line) % 2 == 0
        for x in range(0, len(line), 2):
            pair = line[x : x + 2]
            if pair == '##':
                yield x + 1
                yield x + 1
            elif pair == '.#':
                yield x + 2
                yield x + 2
            elif pair == '#.':
                yield x - 1
                yield x - 1
            elif pair == '..':
                yield x + 3
                yield x + 3

def print_input(values):
    curr = 1
    n = 0
    for x in values:
        if x == curr:
            n += 1
        else:
            assert n >= 2
            for _ in range(n - 2):
                print('noop')
            print('addx', x - curr)
            curr = x
            n = 1
    for _ in range(n):
        print('noop')
        
if __name__ == '__main__':
    main()
