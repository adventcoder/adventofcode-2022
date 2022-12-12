
import framework
from collections import deque
from functools import reduce
from math import lcm

def solve(input):
    monkeys = tuple(map(Monkey, input.split('\n\n')))
    yield monkey_business(monkeys, 20, lambda worry: worry // 3)
    modulus = reduce(lcm, [monkey.test for monkey in monkeys], 1)
    yield monkey_business(monkeys, 10000, lambda worry: worry % modulus)

def parse_op(expr):
    tokens = expr.split()
    assert tokens[0] == 'old'
    if tokens[2] == tokens[0]:
        return { '+': lambda old: old + old, '*': lambda old: old * old }[tokens[1]]
    else:
        x = int(tokens[2])
        return { '+': lambda old: old + x, '*': lambda old: old * x }[tokens[1]]

class Monkey:
    def __init__(self, chunk):
        for line in chunk.splitlines():
            label, value = line.lstrip().split(':', 2)
            if label == 'Starting items':
                self.starting_items = list(map(int, value.split(',')))
            elif label == 'Operation':
                self.inspect = parse_op(value.split('=')[1])
            elif label == 'Test':
                self.test = int(value.split()[-1])
            elif label == 'If true':
                self.index_if_true = int(value.split()[-1])
            elif label == 'If false':
                self.index_if_false = int(value.split()[-1])

    def throw_index(self, item):
        return self.index_if_true if item % self.test == 0 else self.index_if_false

def monkey_business(monkeys, rounds, relief):
    queues = [deque(monkey.starting_items) for monkey in monkeys]
    inspections = [0] * len(monkeys)
    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            while queues[i]:
                item = queues[i].popleft()
                new_item = relief(monkey.inspect(item))
                inspections[i] += 1
                queues[monkey.throw_index(new_item)].append(new_item)
    inspections.sort(reverse = True)
    return inspections[0] * inspections[1]

if __name__ == '__main__':
    framework.main()
