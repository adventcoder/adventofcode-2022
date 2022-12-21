import framework
import re
from collections import defaultdict, namedtuple
from math import *

# TODO: this is kind of messy and could be a bit faster maybe.
def solve(input):
    blueprints = [Blueprint(line) for line in input.splitlines()]
    yield sum(bp.num * astar(24, bp) for bp in blueprints)
    yield prod(astar(32, bp) for bp in blueprints[:3])

class Blueprint:
    def __init__(self, line):
        self.num, a, b, c, d, e, f = map(int, re.findall(r'\d+', line))
        self.costs = [(a, 0, 0, 0), (b, 0, 0, 0), (c, d, 0, 0), (e, 0, f, 0)]
        self.max_cost = [max(a, b, c, e), d, f]

def astar(time, blueprint):
    start = State((0, 0, 0, 0), (1, 0, 0, 0), time)
    best = {}
    best[inputs(start)] = start
    queue = defaultdict(set)
    queue[heuristic(start)].add(start)
    while queue:
        max_key = max(queue.keys())
        curr = queue[max_key].pop()
        if not queue[max_key]:
            del queue[max_key]
        if curr.time == 0:
            return curr.resources[3]
        for next in neighbours(curr, blueprint):
            key = inputs(next)
            if key not in best:
                best[key] = next
                queue[heuristic(next)].add(next)
            else:
                prev = best[key]
                if next.resources[3] > prev.resources[3]:
                    queue[heuristic(prev)].remove(prev)
                    best[key] = next
                    queue[heuristic(next)].add(next)

State = namedtuple('State', ['resources', 'robots', 'time'])

def inputs(st):
    return (st.resources[:3], st.robots, st.time)

def heuristic(st):
    return st.resources[3] + st.robots[3] * st.time + st.time*(st.time-1)//2

def neighbours(st, bp):
    bought_any = False
    for i in range(4):
        if worth_buying(st, bp, i):
            time = time_to_wait(st, bp, i)
            if time + 1 < st.time:
                yield wait_then_buy(st, bp, i, time)
                bought_any = True
    if not bought_any:
        yield wait(st)

def worth_buying(st, bp, i):
    return i == 3 or st.resources[i] + st.robots[i] * st.time < bp.max_cost[i] * st.time

def time_to_wait(st, bp, i):
    max_time = 0
    for j in range(4):
        if st.resources[j] < bp.costs[i][j]:
            if st.robots[j] == 0:
                return inf
            time = ceil((bp.costs[i][j] - st.resources[j]) / st.robots[j])
            max_time = max(max_time, time)
    return max_time

def wait(st):
    return State(tuple(st.resources[j] + st.robots[j] * st.time for j in range(4)), st.robots, 0)

def wait_then_buy(st, bp, i, time):
    return State(tuple(st.resources[j] + st.robots[j] * (time + 1) - bp.costs[i][j] for j in range(4)),
                 tuple(st.robots[j] + (i == j) for j in range(4)),
                 st.time - time - 1)

if __name__ == '__main__':
    framework.main()
