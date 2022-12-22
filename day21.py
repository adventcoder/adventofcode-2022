import framework
from operator import *

def flip(op):
    return lambda x, y: op(y, x)

ops = { '+': add, '-': sub, '*': mul, '/': floordiv }
left_inverse = { '+': sub, '-': add, '*': floordiv, '/': mul }
right_inverse = { '+': sub, '-': flip(sub), '*': floordiv, '/': flip(floordiv) }

def solve(input):
    monkeys = parse_monkeys(input)
    yield speak('root', monkeys)
    yield should_say('humn', monkeys, reverse(monkeys))

def parse_monkeys(input):
    monkeys = {}
    for line in input.splitlines():
        name, expr = line.split(':')
        tokens = expr.split()
        monkeys[name] = int(tokens[0]) if len(tokens) == 1 else tokens
    return monkeys

def speak(name, monkeys):
    monkey = monkeys[name]
    if isinstance(monkey, int):
        return monkey
    else:
        left, opname, right = monkey
        return ops[opname](speak(left, monkeys), speak(right, monkeys))

def should_say(name, monkeys, parents):
    parent = parents[name]
    left, opname, right = monkeys[parent]
    if parent == 'root':
        if name == left:
            return speak(right, monkeys)
        elif name == right:
            return speak(left, monkeys)
    else:
        if name == left:
            return left_inverse[opname](should_say(parent, monkeys, parents), speak(right, monkeys))
        elif name == right:
            return right_inverse[opname](should_say(parent, monkeys, parents), speak(left, monkeys))

def reverse(monkeys):
    parents = {}
    for name, monkey in monkeys.items():
        if not isinstance(monkey, int):
            left, _, right = monkey
            parents[left] = name
            parents[right] = name
    return parents

if __name__ == '__main__':
    framework.main()
