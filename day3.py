
import framework
from utils import parse_list, groups
from functools import reduce

def solve(input):
    bags = parse_list(input)
    yield sum(priority(badge(compartments(bag))) for bag in bags)
    yield sum(priority(badge(group)) for group in groups(bags, 3))

def compartments(bag):
    return groups(bag, len(bag) // 2)

def badge(group):
    return next(iter(reduce(set.intersection, map(set, group))))

def priority(item):
    return 26 * item.isupper() + ord(item.lower()) - ord('a') + 1

if __name__ == '__main__':
    framework.main()
