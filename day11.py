
import framework
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
                self.op = parse_op(value.split('=')[1])
            elif label == 'Test':
                self.test = int(value.split()[-1])
            elif label == 'If true':
                self.index_if_true = int(value.split()[-1])
            elif label == 'If false':
                self.index_if_false = int(value.split()[-1])

    def throw_index(self, item):
        return self.index_if_true if item % self.test == 0 else self.index_if_false

def monkey_business(monkeys, rounds, relief):
    inspections = [0] * len(monkeys)
    for starting_index, monkey in enumerate(monkeys):
        for item in monkey.starting_items:
            index = starting_index
            for _ in range(rounds):
                # An item can be processed multiple times in a single round if new index >= orig index
                # TODO: cycle detection? memoization?
                while True:
                    inspections[index] += 1
                    orig_index = index
                    item = relief(monkeys[index].op(item))
                    index = monkeys[index].throw_index(item)
                    if index < orig_index:
                        break
    inspections.sort(reverse = True)
    return inspections[0] * inspections[1]

if __name__ == '__main__':
    framework.main()
