
import framework
from functools import reduce

def solve(input):
    chunks = input.split('\n\n')
    stacks = parse_stacks(chunks[0])
    moves = parse_moves(chunks[1])
    yield top(stacks, moves, move1)
    yield top(stacks, moves, move2)

def top(stacks, moves, proc):
    result = [stack.copy() for stack in stacks]
    for move in moves:
        proc(result, *move)
    return ''.join([stack[-1] for stack in result])

def move1(stacks, n, src, dst):
    for _ in range(n):
        stacks[dst - 1].append(stacks[src - 1].pop())

def move2(stacks, n, src, dst):
    stacks[dst - 1].extend(stacks[src - 1][-n : ])
    del stacks[src - 1][-n : ]

def parse_stacks(chunk):
    stacks = []
    for line in chunk.splitlines():
        n = (len(line) + 1) // 4
        while len(stacks) < n:
            stacks.append([])
        for i in range(n):
            c = line[4 * i + 1]
            if c != ' ':
                stacks[i].append(c)
    for i, stack in enumerate(stacks):
        n = int(stack.pop())
        assert i + 1 == n
        stack.reverse()
    return stacks

def print_stacks(stacks):
    height = max(len(stack) for stack in stacks)
    for i in reversed(range(height)):
        print(' '.join('[' + stack[i] + ']' if i < len(stack) else '   ' for stack in stacks))
    print(' '.join(str(i + 1).center(3) for i in range(len(stacks))))

def parse_moves(chunk):
    return list(map(parse_move, chunk.splitlines()))

def parse_move(line):
    return [int(token) for token in line.split() if token.isdigit()]

if __name__ == '__main__':
    framework.main()
