
import framework

def solve(input):
    chunks = input.split('\n\n')
    stacks = parse_stacks(chunks[0])
    instructions = list(map(parse_instruction, chunks[1].splitlines()))
    yield top(apply(stacks, instructions, move1))
    yield top(apply(stacks, instructions, move2))

def apply(stacks, instructions, move, debug = False):
    result = [stack.copy() for stack in stacks]
    if debug:
        print_stacks(result)
    for n, i, j in instructions:
        move(result, n, i, j)
        if debug:
            import os, time
            time.sleep(0.1)
            os.system('cls')
            print_stacks(result)
    return result

def move1(stacks, n, i, j):
    for _ in range(n):
        stacks[j - 1].append(stacks[i - 1].pop())

def move2(stacks, n, i, j):
    crates = stacks[i - 1][-n : ]
    del stacks[i - 1][-n : ]
    stacks[j - 1].extend(crates)

def top(stacks):
    return ''.join([stack[-1] for stack in stacks])

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

def parse_instruction(line):
    return [int(token) for token in line.split() if token.isdigit()]

if __name__ == '__main__':
    framework.main()
