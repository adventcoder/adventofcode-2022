
import framework
from math import lcm, prod
from collections import Counter, namedtuple

def solve(input):
    monkeys = [parse_monkey(chunk) for chunk in input.split('\n\n')]
    yield monkey_business(monkeys, 20, lambda worry: worry // 3)
    modulus = lcm(*(monkey.test for monkey in monkeys))
    yield monkey_business(monkeys, 10000, lambda worry: worry % modulus)

Monkey = namedtuple('Monkey', ['starting_items', 'op', 'test', 'index_if_true', 'index_if_false'])

def parse_monkey(chunk):
    lines = chunk.splitlines()
    values = [line.split(':', 2)[1] for line in lines[1 : ]]
    starting_items = list(map(int, values[0].split(',')))
    op = parse_op(values[1].split('=')[1])
    test = int(values[2].split()[-1])
    index_if_true = int(values[3].split()[-1])
    index_if_false = int(values[4].split()[-1])
    return Monkey(starting_items, op, test, index_if_true, index_if_false)

def parse_op(expr):
    tokens = expr.split()
    assert tokens[0] == 'old'
    if tokens[2] == tokens[0]:
        return { '+': lambda old: old + old, '*': lambda old: old * old }[tokens[1]]
    else:
        x = int(tokens[2])
        return { '+': lambda old: old + x, '*': lambda old: old * x }[tokens[1]]

def monkey_business(monkeys, rounds, relief):
    return prod(count for _, count in inspections(monkeys, rounds, relief).most_common(2))

def inspections(monkeys, rounds, relief):
    total = Counter()
    for index, monkey in enumerate(monkeys):
        for worry in monkey.starting_items:
            total += item_inspections(monkeys, index, worry, rounds, relief)
    return total

def item_inspections(monkeys, index, worry, rounds, relief):
    seen = {}
    totals = [Counter()]
    for round in range(rounds):
        key = (index, worry)
        if key in seen:
            prev_round = seen[key]
            q, r = divmod(rounds - prev_round, round - prev_round)
            diffs = totals[round] - totals[prev_round]
            for index in diffs:
                diffs[index] *= q
            return totals[prev_round + r] + diffs
        seen[key] = round
        counts = totals[-1].copy()
        # It's possible for multiple monkeys to inspect an item in a single round as long as the item keeps being passed to a monkey with a higher index
        prev_index = 0
        while index >= prev_index:
            monkey = monkeys[index]
            counts[index] += 1
            prev_index = index
            worry = relief(monkey.op(worry))
            index = monkey.index_if_true if worry % monkey.test == 0 else monkey.index_if_false
        totals.append(counts)
    return totals[rounds]

if __name__ == '__main__':
    framework.main()
