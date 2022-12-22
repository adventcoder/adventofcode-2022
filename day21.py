import framework
from operator import *
from collections import namedtuple

def flip(op):
    return lambda x, y: op(y, x)

Operator = namedtuple('Operator', ['apply', 'left_inv', 'right_inv'])

operators = {
    '+': Operator(add, sub, sub),
    '-': Operator(sub, add, flip(sub)),
    '*': Operator(mul, floordiv, floordiv),
    '/': Operator(floordiv, mul, flip(floordiv))
}

Const = namedtuple('Const', ['value'])
Expr = namedtuple('Expr', ['left', 'op', 'right'])
Monkey = Expr | Const

def solve(input):
    monkeys = parse_monkeys(input)
    yield speak('root', monkeys)
    yield should_say('humn', monkeys, reverse(monkeys))

def parse_monkeys(input):
    monkeys = {}
    for line in input.splitlines():
        name, expr = line.split(':')
        tokens = expr.split()
        if len(tokens) == 1:
            monkeys[name] = Const(int(tokens[0]))
        else:
            monkeys[name] = Expr(tokens[0], operators.get(tokens[1]), tokens[2])
    return monkeys

def reverse(monkeys):
    parent_names = {}
    for name, monkey in monkeys.items():
        match monkey:
            case Expr(left, _, right):
                parent_names[left] = name
                parent_names[right] = name
    return parent_names

def speak(name, monkeys):
    match monkeys[name]:
        case Const(value):
            return value
        case Expr(left, op, right):
            return op.apply(speak(left, monkeys), speak(right, monkeys))

def should_say(name, monkeys, parent_names):
    parent_name = parent_names[name]
    parent = monkeys[parent_name]
    if parent_name == 'root':
        if name == parent.left:
            return speak(parent.right, monkeys)
        elif name == parent.right:
            return speak(parent.left, monkeys)
    else:
        answer = should_say(parent_name, monkeys, parent_names)
        if name == parent.left:
            return parent.op.left_inv(answer, speak(parent.right, monkeys))
        elif name == parent.right:
            return parent.op.right_inv(answer, speak(parent.left, monkeys))

if __name__ == '__main__':
    framework.main()
