
import framework

def solve(input):
    chunks = input.split('\n\n')
    stacks = parse_stacks(chunks[0])
    moves = parse_moves(chunks[1])
    yield top(apply1(stacks, moves))
    yield top(apply2(stacks, moves))

def top(stacks):
    return ''.join([stack[-1] for stack in stacks])

def apply1(stacks, moves):
    result = [stack.copy() for stack in stacks]
    for n, src, dst in moves:
        for _ in range(n):
            result[dst - 1].append(result[src - 1].pop())
    return result

def apply2(stacks, moves):
    result = [stack.copy() for stack in stacks]
    for n, src, dst in moves:
        result[dst - 1].extend(result[src - 1][-n : ])
        del result[src - 1][-n : ]
    return result

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
