
import framework
from utils import groups

def solve(input):
    chunks = input.split('\n\n')
    stacks = parse_stacks(chunks[0])
    moves = parse_moves(chunks[1])
    yield top(stacks, moves, move1)
    yield top(stacks, moves, move2)

def top(stacks, moves, op):
    result = [stack.copy() for stack in stacks]
    for move in moves:
        op(result, *move)
    return ''.join([stack[-1][1 : -1] for stack in result])

def move1(stacks, n, src, dst):
    for _ in range(n):
        stacks[dst - 1].append(stacks[src - 1].pop())

def move2(stacks, n, src, dst):
    stacks[dst - 1].extend(stacks[src - 1][-n : ])
    del stacks[src - 1][-n : ]

def parse_stacks(chunk):
    rows = [[group.strip() for group in groups(line, 4)] for line in chunk.splitlines()]
    for i, label in enumerate(rows.pop()):
        assert i == int(label) - 1
    stacks = [list(reversed(col)) for col in zip(*rows)]
    for stack in stacks:
        while not stack[-1]:
            stack.pop()
    return stacks

def parse_moves(chunk):
    return list(map(parse_move, chunk.splitlines()))

def parse_move(line):
    return [int(token) for token in line.split() if token.isdigit()]

if __name__ == '__main__':
    framework.main()
