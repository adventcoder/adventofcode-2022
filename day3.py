
from utils import read_list
from functools import reduce

def main():
    bags = read_list('inputs/day3.txt')
    print('Silver:', sum(priority(badge(compartments(bag))) for bag in bags))
    print('Gold:', sum(priority(badge(group)) for group in groups(bags)))

def compartments(bag):
    i = len(bag) // 2
    return bag[0 : i], bag[i : ]

def groups(bags):
    return (bags[i : i + 3] for i in range(0, len(bags), 3))

def badge(group):
    return next(iter(reduce(set.intersection, map(set, group))))

def priority(item):
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    if 'A' <= item <= 'Z':
        return ord(item) - ord('A') + 27
    raise(ValueError('invalid item: {}'.format(item)))

if __name__ == '__main__':
    main()
