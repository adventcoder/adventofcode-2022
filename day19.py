import framework
import re
from collections import defaultdict, namedtuple
from math import prod, inf

# TODO: this is kind of messy and could be a bit faster maybe.
def solve(input):
    blueprints = [Blueprint(line) for line in input.splitlines()]
    yield sum(bp.num * search(24, bp) for bp in blueprints)
    yield prod(search(32, bp) for bp in blueprints[:3])

class Blueprint:
    def __init__(self, line):
        self.num, a, b, c, d, e, f = map(int, re.findall(r'\d+', line))
        self.costs = [(a, 0, 0), (b, 0, 0), (c, d, 0), (e, 0, f)]
        self.max_cost = [max(a, b, c, e), d, f]

def search(time, bp):
    start = State((0, 0, 0), (1, 0, 0, 0), time)
    geodes = { start: 0 }
    queue = defaultdict(set)
    queue[start.heuristic(bp)].add(start)
    while queue:
        max_key = max(queue.keys())
        curr = queue[max_key].pop()
        if not queue[max_key]:
            del queue[max_key]
        if curr.time == 0:
            return geodes[curr]
        for next, geodes_diff in curr.neighbours(bp):
            new_geodes = geodes[curr] + geodes_diff
            if next not in geodes:
                geodes[next] = new_geodes
                queue[new_geodes + next.heuristic(bp)].add(next)
            elif new_geodes > geodes[next]:
                queue[geodes[next] + next.heuristic(bp)].remove(next)
                geodes[next] = new_geodes
                queue[new_geodes + next.heuristic(bp)].add(next)

class State(namedtuple('State', ['resource', 'robot', 'time'])):
    def heuristic(self, bp):
        return self.robot[3] * self.time + self.time*(self.time-1)//2

    def neighbours(self, bp):
        nothing_to_buy = True
        for i in range(4):
            if self.worth_buying(bp, i):
                time = self.time_to_wait(bp, i)
                if time + 1 < self.time:
                    yield self.wait_then_buy(time, bp, i)
                    nothing_to_buy = False
        if nothing_to_buy:
            yield self.wait(self.time)

    def worth_buying(self, bp, i):
        # resource we currently produce < most resource we'll ever need
        return i == 3 or self.resource[i] + self.robot[i] * self.time < bp.max_cost[i] * self.time

    def time_to_wait(self, bp, i):
        max_time = 0
        for j in range(3):
            if self.resource[j] < bp.costs[i][j]:
                if self.robot[j] == 0:
                    return inf
                max_time = max(max_time, (bp.costs[i][j] - self.resource[j] + self.robot[j] - 1) // self.robot[j])
        return max_time

    def wait(self, time):
        resource = tuple(self.resource[j] + self.robot[j] * time for j in range(3))
        return State(resource, self.robot, self.time - time), self.robot[3] * time

    def wait_then_buy(self, time, bp, i):
        resource = tuple(self.resource[j] - bp.costs[i][j] + self.robot[j] * (time + 1) for j in range(3))
        robot = tuple(self.robot[j] + (i == j) for j in range(4))
        return State(resource, robot, self.time - time - 1), self.robot[3] * (time + 1)

if __name__ == '__main__':
    framework.main()
