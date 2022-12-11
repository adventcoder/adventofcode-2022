
import framework
from utils import product

def solve(input):
    yield part1(input)
    yield part2(input)

def part1(input):
    troop = list(map(Monkey, input.split('\n\n')))
    for _ in range(20):
        for monkey in troop:
           monkey.turn(troop, lambda worry: worry // 3)
    troop.sort(key = lambda m: m.inspected)
    return troop[-1].inspected * troop[-2].inspected

def part2(input):
    troop = list(map(Monkey, input.split('\n\n')))
    modulus = product(monkey.test for monkey in troop)
    for _ in range(10000):
        for monkey in troop:
           monkey.turn(troop, lambda worry: worry % modulus)
    troop.sort(key = lambda m: m.inspected)
    return troop[-1].inspected * troop[-2].inspected

class Monkey:
    def __init__(self, chunk):
        for line in chunk.splitlines():
            label, value = line.lstrip().split(':', 2)
            if label == 'Starting items':
                self.items = list(map(int, value.split(',')))
            elif label == 'Operation':
                self.op = value.strip()
            elif label == 'Test':
                self.test = int(value.split()[-1])
            elif label == 'If true':
                self.index_if_true = int(value.split()[-1])
            elif label == 'If false':
                self.index_if_false = int(value.split()[-1])
        self.inspected = 0

    def operate(self, item):
        vars = { 'old': item }
        exec(self.op, None, vars)
        return vars['new']

    def turn(self, troop, relief_management):
        while self.items:
            item = relief_management(self.operate(self.items.pop(0)))
            self.inspected += 1
            if item % self.test == 0:
                troop[self.index_if_true].items.append(item)
            else:
                troop[self.index_if_false].items.append(item)

if __name__ == '__main__':
    framework.main()
